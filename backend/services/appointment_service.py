"""
MediConnect HMS — Appointment Service
Business logic and persistence for outpatient appointments and queue tokens.
"""

import json
from datetime import datetime
from db.connection import get_db


def get_appointments(role='doctor', user_id=None):
    """Fetch appointments, masking sensitive PHI if accessed by admin role."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM appointments ORDER BY created_at DESC')
    rows = []
    for r in c.fetchall():
        a = dict(r)
        a['patientName'] = a.get('patient_name')
        a['doctorName'] = a.get('doctor_name')
        a['tokenNumber'] = a.get('token_number')
        a['patientAge'] = a.get('patient_age')
        a['patientGender'] = a.get('patient_gender')
        a['patientPhone'] = a.get('patient_phone')
        a['historySummary'] = a.get('history_summary')
        try:
            a['vitals'] = json.loads(a.get('vitals', '{}'))
        except Exception:
            a['vitals'] = {}

        if role == 'admin':
            a['symptoms'] = "🔒 [Restricted] Confidential PHI - Hidden from Admin"
            a['historySummary'] = "🔒 [Restricted] Medical history accessible only by treating physician."
        
        rows.append(a)
    conn.close()
    return rows


def get_appointment_by_id(apt_id):
    """Fetch a single appointment by ID."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM appointments WHERE id=?', (apt_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    a = dict(row)
    a['patientName'] = a.get('patient_name')
    a['doctorName'] = a.get('doctor_name')
    a['tokenNumber'] = a.get('token_number')
    try:
        a['vitals'] = json.loads(a.get('vitals', '{}'))
    except Exception:
        a['vitals'] = {}
    return a


def create_appointment(data):
    """Schedule and record a new appointment."""
    conn = get_db()
    c = conn.cursor()
    apt_id = data.get('id') or f"apt-{int(datetime.now().timestamp())}"
    token_num = data.get('tokenNumber') or f"T-{int(datetime.now().timestamp()) % 1000:03d}"
    vitals_json = json.dumps(data.get('vitals', {}))
    now = datetime.now().isoformat()
    
    slot_val = data.get('slot') or data.get('timeSlot') or data.get('time', '10:00 AM')
    dept_val = data.get('department') or data.get('doctorSpecialty') or data.get('specialty', 'General Medicine')

    c.execute('''
    INSERT INTO appointments (id, patient_id, patient_name, patient_age, patient_gender, patient_phone,
                              doctor_id, doctor_name, department, date, time, slot, status,
                              token_number, type, symptoms, history_summary, vitals, notes, created_at)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        apt_id,
        data.get('patientId', 'pat-1'),
        data.get('patientName', 'Tushar Tawar'),
        data.get('patientAge', 32),
        data.get('patientGender', 'Male'),
        data.get('patientPhone', '+91 98765 43210'),
        data.get('doctorId'),
        data.get('doctorName'),
        dept_val,
        data.get('date'),
        data.get('time', slot_val),
        slot_val,
        data.get('status', 'Scheduled'),
        token_num,
        data.get('type', 'In-Person'),
        data.get('symptoms', ''),
        data.get('historySummary', ''),
        vitals_json,
        data.get('notes', ''),
        now
    ))
    conn.commit()
    conn.close()
    result = dict(data)
    result['id'] = apt_id
    result['tokenNumber'] = token_num
    return result


def update_appointment_status(apt_id, status):
    """Update appointment status (e.g., Scheduled, In Progress, Completed, Cancelled)."""
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE appointments SET status=? WHERE id=?', (status, apt_id))
    conn.commit()
    conn.close()
    return {'id': apt_id, 'status': status}


def delete_appointment(apt_id):
    """Delete an appointment by ID."""
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM appointments WHERE id=?', (apt_id,))
    conn.commit()
    conn.close()
    return {'success': True, 'id': apt_id}
