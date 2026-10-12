"""
MediConnect HMS — Patient Service
Business logic and persistence for patient profiles, medical history, and privacy settings.
"""

import json
from datetime import datetime
from db.connection import get_db


def _parse_patient(row):
    """Normalize SQLite row into front-end compatible patient dictionary."""
    if not row:
        return None
    p = dict(row)
    p['bloodGroup'] = p.get('blood_group')
    p['emergencyContact'] = p.get('emergency_contact')
    p['securityPin'] = p.get('security_pin')
    try:
        p['allergies'] = json.loads(p.get('allergies', '[]'))
    except Exception:
        p['allergies'] = ['Penicillin']
    try:
        p['chronicConditions'] = json.loads(p.get('chronic_conditions', '[]'))
    except Exception:
        p['chronicConditions'] = []
    try:
        p['privacySettings'] = json.loads(p.get('privacy_settings', '{}'))
    except Exception:
        p['privacySettings'] = {}
    return p


def get_patients():
    """Fetch all patients."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM patients')
    rows = [_parse_patient(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_patient(patient_id='pat-1'):
    """Fetch single patient by ID, fallback to first available if not found."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM patients WHERE id=?', (patient_id,))
    row = c.fetchone()
    if not row:
        c.execute('SELECT * FROM patients LIMIT 1')
        row = c.fetchone()
    conn.close()
    return _parse_patient(row)


def add_patient(data):
    """Create a new patient record."""
    conn = get_db()
    c = conn.cursor()
    pat_id = data.get('id') or f"pat-{int(datetime.now().timestamp())}"
    uhid = data.get('uhid') or f"MC-2026-{int(datetime.now().timestamp()) % 10000:04d}"
    allergies = json.dumps(data.get('allergies', [])) if isinstance(data.get('allergies'), list) else data.get('allergies', '[]')
    chronic = json.dumps(data.get('chronicConditions', [])) if isinstance(data.get('chronicConditions'), list) else data.get('chronicConditions', '[]')
    privacy = json.dumps(data.get('privacySettings', {})) if isinstance(data.get('privacySettings'), dict) else data.get('privacySettings', '{}')

    c.execute('''
    INSERT INTO patients (id, name, uhid, age, gender, blood_group, phone, email, abha_id, emergency_contact, address, allergies, chronic_conditions, security_pin, privacy_settings)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        pat_id,
        data.get('name'),
        uhid,
        data.get('age', 30),
        data.get('gender', 'Male'),
        data.get('bloodGroup', 'O+'),
        data.get('phone'),
        data.get('email'),
        data.get('abhaId', ''),
        data.get('emergencyContact', ''),
        data.get('address', ''),
        allergies,
        chronic,
        data.get('securityPin', '1234'),
        privacy
    ))
    conn.commit()
    conn.close()
    return get_patient(pat_id)


def update_patient(patient_id, data):
    """Update patient demographic and clinical details."""
    conn = get_db()
    c = conn.cursor()
    allergies = json.dumps(data.get('allergies', [])) if isinstance(data.get('allergies'), list) else data.get('allergies')
    chronic = json.dumps(data.get('chronicConditions', [])) if isinstance(data.get('chronicConditions'), list) else data.get('chronicConditions')
    privacy = json.dumps(data.get('privacySettings', {})) if isinstance(data.get('privacySettings'), dict) else data.get('privacySettings')
    
    c.execute('''
    UPDATE patients SET name=COALESCE(?, name),
                        age=COALESCE(?, age),
                        gender=COALESCE(?, gender),
                        blood_group=COALESCE(?, blood_group),
                        phone=COALESCE(?, phone),
                        email=COALESCE(?, email),
                        emergency_contact=COALESCE(?, emergency_contact),
                        address=COALESCE(?, address),
                        allergies=COALESCE(?, allergies),
                        chronic_conditions=COALESCE(?, chronic_conditions),
                        security_pin=COALESCE(?, security_pin),
                        privacy_settings=COALESCE(?, privacy_settings)
    WHERE id=?
    ''', (
        data.get('name'),
        data.get('age'),
        data.get('gender'),
        data.get('bloodGroup'),
        data.get('phone'),
        data.get('email'),
        data.get('emergencyContact'),
        data.get('address'),
        allergies,
        chronic,
        data.get('securityPin'),
        privacy,
        patient_id
    ))
    conn.commit()
    conn.close()
    return get_patient(patient_id)


def delete_patient(patient_id):
    """Delete a patient record."""
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM patients WHERE id=?', (patient_id,))
    conn.commit()
    conn.close()
    return {'success': True, 'id': patient_id}
