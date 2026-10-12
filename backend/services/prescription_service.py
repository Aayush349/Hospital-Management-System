"""
MediConnect HMS — Prescription Service
Business logic and persistence for doctor prescriptions and medications.
"""

import json
from datetime import datetime
from db.connection import get_db


def get_prescriptions(role='doctor'):
    """Fetch clinical prescriptions. Returns empty list for admin role due to strict PHI isolation."""
    if role == 'admin':
        return []

    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM prescriptions ORDER BY created_at DESC')
    rows = []
    for r in c.fetchall():
        rx = dict(r)
        rx['patientName'] = rx.get('patient_name')
        rx['doctorName'] = rx.get('doctor_name')
        rx['followUp'] = rx.get('follow_up')
        try:
            rx['medicines'] = json.loads(rx.get('medicines', '[]'))
        except Exception:
            rx['medicines'] = []
        try:
            rx['vitals'] = json.loads(rx.get('vitals', '{}'))
        except Exception:
            rx['vitals'] = {}
        rows.append(rx)
    conn.close()
    return rows


def get_prescription_by_id(rx_id):
    """Fetch single prescription by ID."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM prescriptions WHERE id=?', (rx_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    rx = dict(row)
    rx['patientName'] = rx.get('patient_name')
    rx['doctorName'] = rx.get('doctor_name')
    rx['followUp'] = rx.get('follow_up')
    try:
        rx['medicines'] = json.loads(rx.get('medicines', '[]'))
    except Exception:
        rx['medicines'] = []
    try:
        rx['vitals'] = json.loads(rx.get('vitals', '{}'))
    except Exception:
        rx['vitals'] = {}
    return rx


def create_prescription(data):
    """Create a new prescription and optionally auto-complete the related appointment."""
    conn = get_db()
    c = conn.cursor()
    rx_id = data.get('id') or f"rx-{int(datetime.now().timestamp())}"
    meds = json.dumps(data.get('medicines', []))
    vitals = json.dumps(data.get('vitals', {}))
    now = datetime.now().isoformat()
    
    c.execute('''
    INSERT INTO prescriptions (id, appointment_id, patient_id, patient_name, doctor_id, doctor_name,
                               date, diagnosis, vitals, medicines, advice, follow_up, created_at)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        rx_id,
        data.get('appointmentId'),
        data.get('patientId', 'pat-1'),
        data.get('patientName', 'Tushar Tawar'),
        data.get('doctorId'),
        data.get('doctorName'),
        data.get('date'),
        data.get('diagnosis'),
        vitals,
        meds,
        data.get('advice'),
        data.get('followUp'),
        now
    ))
    
    if data.get('appointmentId'):
        c.execute('UPDATE appointments SET status=? WHERE id=?', ('Completed', data.get('appointmentId')))

    conn.commit()
    conn.close()
    result = dict(data)
    result['id'] = rx_id
    return result


def delete_prescription(rx_id):
    """Delete a prescription by ID."""
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM prescriptions WHERE id=?', (rx_id,))
    conn.commit()
    conn.close()
    return {'success': True, 'id': rx_id}
