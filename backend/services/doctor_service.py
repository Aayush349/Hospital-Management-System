"""
MediConnect HMS — Doctor Service
Business logic and persistence for doctor profiles and directories.
"""

import json
from datetime import datetime
from db.connection import get_db


def get_doctors():
    """Fetch all doctors with parsed JSON fields."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM doctors')
    rows = []
    for r in c.fetchall():
        d = dict(r)
        if d.get('available_days'):
            try:
                d['availableDays'] = json.loads(d['available_days'])
            except Exception:
                d['availableDays'] = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        d['roomNo'] = d.get('room_no')
        rows.append(d)
    conn.close()
    return rows


def get_doctor_by_id(doc_id):
    """Fetch a single doctor by ID."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM doctors WHERE id=?', (doc_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    if d.get('available_days'):
        try:
            d['availableDays'] = json.loads(d['available_days'])
        except Exception:
            d['availableDays'] = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    d['roomNo'] = d.get('room_no')
    return d


def add_doctor(data):
    """Register a new doctor."""
    conn = get_db()
    c = conn.cursor()
    doc_id = data.get('id') or f"doc-{int(datetime.now().timestamp())}"
    avail = json.dumps(data.get('availableDays', ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']))
    c.execute('''
    INSERT INTO doctors (id, name, email, phone, department, specialization, experience, qualification, room_no, fee, available_days, image, about)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        doc_id,
        data.get('name'),
        data.get('email'),
        data.get('phone'),
        data.get('department'),
        data.get('specialization'),
        data.get('experience', 5),
        data.get('qualification'),
        data.get('roomNo', 'Room 101'),
        data.get('fee', 500),
        avail,
        data.get('image', 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&q=80&w=300'),
        data.get('about', 'Senior Medical Practitioner')
    ))
    conn.commit()
    conn.close()
    result = dict(data)
    result['id'] = doc_id
    return result


def update_doctor(doc_id, data):
    """Update doctor profile."""
    conn = get_db()
    c = conn.cursor()
    avail = json.dumps(data.get('availableDays', ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'])) if data.get('availableDays') is not None else None
    
    # Existing doctor
    current = get_doctor_by_id(doc_id)
    if not current:
        conn.close()
        return None

    c.execute('''
    UPDATE doctors SET name=COALESCE(?, name),
                       email=COALESCE(?, email),
                       phone=COALESCE(?, phone),
                       department=COALESCE(?, department),
                       specialization=COALESCE(?, specialization),
                       experience=COALESCE(?, experience),
                       qualification=COALESCE(?, qualification),
                       room_no=COALESCE(?, room_no),
                       fee=COALESCE(?, fee),
                       available_days=COALESCE(?, available_days),
                       image=COALESCE(?, image),
                       about=COALESCE(?, about)
    WHERE id=?
    ''', (
        data.get('name'),
        data.get('email'),
        data.get('phone'),
        data.get('department'),
        data.get('specialization'),
        data.get('experience'),
        data.get('qualification'),
        data.get('roomNo'),
        data.get('fee'),
        avail,
        data.get('image'),
        data.get('about'),
        doc_id
    ))
    conn.commit()
    conn.close()
    return get_doctor_by_id(doc_id)


def delete_doctor(doc_id):
    """Delete a doctor record."""
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM doctors WHERE id=?', (doc_id,))
    conn.commit()
    conn.close()
    return {'success': True, 'id': doc_id}
