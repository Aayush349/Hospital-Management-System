"""
MediConnect HMS — Clinical AI Chat Service
Connects to OpenRouter LLM API with intelligent medical context, multi-turn memory,
robust model fallbacks, and SQLite persistence.
"""

import json
import urllib.request
import urllib.error
from datetime import datetime
from db.connection import get_db
from config import OPENROUTER_API_KEY, OPENROUTER_API_URL, OPENROUTER_MODELS


def get_chat_history(session_id):
    """Retrieve chronologically ordered chat messages for a session."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM chat_messages WHERE session_id=? ORDER BY timestamp ASC', (session_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def save_chat_message(session_id, sender, message, role='patient'):
    """Record a chat message into the database."""
    conn = get_db()
    c = conn.cursor()
    msg_id = f"msg-{int(datetime.now().timestamp() * 1000)}"
    now = datetime.now().isoformat()
    c.execute('''
    INSERT INTO chat_messages (id, session_id, sender, message, role, timestamp)
    VALUES (?,?,?,?,?,?)
    ''', (msg_id, session_id, sender, message, role, now))
    conn.commit()
    conn.close()
    return {
        'id': msg_id,
        'sessionId': session_id,
        'sender': sender,
        'message': message,
        'role': role,
        'timestamp': now
    }


def clear_chat_history(session_id):
    """Delete all chat logs associated with a session ID."""
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM chat_messages WHERE session_id=?', (session_id,))
    conn.commit()
    conn.close()
    return {'success': True}


def _build_system_prompt(context=None):
    """Construct a medical system prompt augmented with live hospital context."""
    system_prompt = (
        "You are MediConnect AI Assistant, an empathetic, highly knowledgeable, and polite clinical assistant "
        "integrated into the MediConnect Hospital Management System.\n"
        "Your capabilities:\n"
        "1. Help patients understand their health questions, symptoms, and potential departments to visit.\n"
        "2. Provide information about hospital services: OPD appointments, doctors, prescriptions, diagnostics, and home sample collection.\n"
        "3. Emphasize that your guidance is for informational purposes and advise consulting a qualified physician for clinical diagnoses.\n"
        "4. In emergencies, urge the patient to call the 24/7 emergency line at 1800-MED-CONNECT or visit Emergency Block E immediately.\n"
        "5. Keep responses concise, well-formatted using clear markdown bullet points and friendly tone.\n"
    )

    if not context or not isinstance(context, dict):
        return system_prompt

    # Append live context if provided
    context_notes = []
    patient = context.get('patient')
    if patient and isinstance(patient, dict):
        name = patient.get('name', 'Patient')
        age = patient.get('age', '')
        allergies = patient.get('allergies', [])
        chronic = patient.get('chronicConditions', [])
        context_notes.append(f"Current Patient: {name}, Age: {age}. Allergies: {allergies}. Chronic conditions: {chronic}.")

    appts = context.get('appointments')
    if appts and isinstance(appts, list):
        upcoming = [f"{a.get('doctorName')} ({a.get('department')}) on {a.get('date')} at {a.get('time')}" for a in appts[:3]]
        if upcoming:
            context_notes.append(f"Upcoming Appointments: {'; '.join(upcoming)}.")

    doctors = context.get('doctors')
    if doctors and isinstance(doctors, list):
        doc_names = [f"{d.get('name')} ({d.get('department')})" for d in doctors[:4]]
        if doc_names:
            context_notes.append(f"Featured Doctors Available: {', '.join(doc_names)}.")

    departments = context.get('departments')
    if departments and isinstance(departments, list):
        dept_names = [d.get('name') for d in departments[:6]]
        if dept_names:
            context_notes.append(f"Hospital Departments: {', '.join(dept_names)}.")

    if context_notes:
        system_prompt += "\nLive Context from MediConnect Database:\n" + "\n".join(f"- {note}" for note in context_notes)

    return system_prompt


def _clinical_fallback_reply(message, context=None):
    """Graceful local fallback if internet or external API is temporarily unavailable."""
    msg = message.lower()
    name = "there"
    if context and isinstance(context, dict) and context.get('patient'):
        name = context['patient'].get('name', 'there').split(' ')[0]

    if any(k in msg for k in ['hi', 'hello', 'hey', 'namaste']):
        return (
            f"Hello **{name}**! 👋 I'm your **MediConnect AI Assistant**.\n\n"
            "How can I assist you today? You can ask about:\n"
            "- 📅 Your appointments\n- 👨‍⚕️ Available doctors\n- 💊 Prescriptions & medications\n"
            "- 🧪 Diagnostic lab tests & home collection\n- 🏥 Hospital timings & emergency care"
        )
    if any(k in msg for k in ['emergency', 'urgent', 'ambulance', '911', '112']):
        return (
            "🚨 **EMERGENCY ASSISTANCE:**\n\n"
            "📞 **24/7 Ambulance Hotline:** 1800-MED-CONNECT\n"
            "🏥 **Emergency Care Ward:** Emergency Block E (Ground Floor)\n\n"
            "For life-threatening emergencies, please dial **112** immediately."
        )
    if any(k in msg for k in ['appoint', 'book', 'schedule', 'slot']):
        return (
            f"📅 To schedule an appointment, **{name}**, you can browse our doctors in the **Patient Portal → Book Appointment** section, "
            "select a preferred time slot, and receive an instant OPD queue token."
        )
    if any(k in msg for k in ['doctor', 'cardiologist', 'physician', 'specialist']):
        return (
            "👨‍⚕️ MediConnect has specialist physicians across Cardiology, Neurology, Orthopedics, "
            "Pediatrics, and General Medicine. You can view all available doctors under **Find Doctors**."
        )
    return (
        f"Thank you for reaching out, **{name}**. I'm here to help with your medical records, "
        "department guidance, lab test bookings, and hospital services. Please let me know how I can help!"
    )


def generate_ai_reply(session_id, user_message, context=None):
    """
    Generate an AI response using OpenRouter.
    Falls back gracefully across models and to local clinical knowledge if network fails.
    """
    if not session_id:
        session_id = f"sess-{int(datetime.now().timestamp())}"

    # 1. Record incoming user message in SQLite
    save_chat_message(session_id, sender='user', message=user_message, role='patient')

    # 2. Retrieve recent conversation history for multi-turn context
    history = get_chat_history(session_id)
    # Take last 6 messages excluding the one just added
    recent_history = history[-7:-1] if len(history) > 1 else []

    messages_payload = [{"role": "system", "content": _build_system_prompt(context)}]
    for h in recent_history:
        role = "assistant" if h.get('sender') == 'bot' or h.get('role') == 'assistant' else "user"
        messages_payload.append({"role": role, "content": h.get('message', '')})
    messages_payload.append({"role": "user", "content": user_message})

    # 3. Call OpenRouter with fallback across candidate models
    ai_reply = None
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost:8000',
        'X-Title': 'MediConnect HMS'
    }

    models_to_try = OPENROUTER_MODELS

    for model_name in models_to_try:
        try:
            req_body = {
                'model': model_name,
                'messages': messages_payload,
                'temperature': 0.7,
                'max_tokens': 800
            }
            req = urllib.request.Request(
                OPENROUTER_API_URL,
                data=json.dumps(req_body).encode('utf-8'),
                headers=headers
            )
            with urllib.request.urlopen(req, timeout=12) as response:
                if response.status == 200:
                    res_json = json.loads(response.read().decode('utf-8'))
                    choices = res_json.get('choices', [])
                    if choices and 'message' in choices[0] and choices[0]['message'].get('content'):
                        ai_reply = choices[0]['message']['content'].strip()
                        break
        except Exception as e:
            # Try next model in candidate list
            continue

    # 4. If all OpenRouter attempts failed or timed out, use intelligent local fallback
    if not ai_reply:
        ai_reply = _clinical_fallback_reply(user_message, context)

    # 5. Save assistant reply in SQLite
    save_chat_message(session_id, sender='bot', message=ai_reply, role='assistant')

    return {
        'reply': ai_reply,
        'sessionId': session_id
    }
