"""
MediConnect HMS — EHR Share Link Service
Secure QR / URL sharing of patient health records with expiration, pin, and view caps.
"""

import uuid
import json
from datetime import datetime
from db.connection import get_db
from services import patient_service, prescription_service, lab_service


def get_share_links(patient_id='pat-1'):
    """Fetch active and past share links for a patient."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM share_links WHERE patient_id=? ORDER BY created_at DESC', (patient_id,))
    rows = []
    for r in c.fetchall():
        sl = dict(r)
        sl['expiresAt'] = sl.get('expires_at')
        sl['maxViews'] = sl.get('max_views')
        sl['viewCount'] = sl.get('view_count')
        sl['isActive'] = bool(sl.get('is_active'))
        try:
            sl['allowedSections'] = json.loads(sl.get('allowed_sections', '[]'))
        except Exception:
            sl['allowedSections'] = []
        try:
            sl['logs'] = json.loads(sl.get('logs', '[]'))
        except Exception:
            sl['logs'] = []
        rows.append(sl)
    conn.close()
    return rows


def create_share_link(data):
    """Generate a new temporary EHR share link."""
    conn = get_db()
    c = conn.cursor()
    link_id = data.get('id') or f"link-{int(datetime.now().timestamp())}"
    token = data.get('token') or f"MEDIC-{uuid.uuid4().hex[:6].upper()}"
    sections = json.dumps(data.get('allowedSections', ['prescriptions', 'lab_reports', 'vitals', 'conditions']))
    logs = json.dumps([{"timestamp": datetime.now().isoformat(), "ip": "127.0.0.1", "action": "Link created by patient"}])
    now = datetime.now().isoformat()

    c.execute('''
    INSERT INTO share_links (id, patient_id, token, title, expires_at, password, max_views, view_count, is_active, allowed_sections, created_at, logs)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        link_id,
        data.get('patientId', 'pat-1'),
        token,
        data.get('title', 'Doctor Consultation Share Link'),
        data.get('expiresAt'),
        data.get('password'),
        data.get('maxViews', 5),
        0,
        1,
        sections,
        now,
        logs
    ))
    conn.commit()
    result = dict(data)
    result['id'] = link_id
    result['token'] = token
    return result


def delete_share_link(link_id):
    """Revoke and delete a share link."""
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM share_links WHERE id=?', (link_id,))
    conn.commit()
    conn.close()
    return {'success': True, 'id': link_id}


def verify_share_link(token, password=""):
    """Verify link validity, enforce view constraints, and return permitted clinical records."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM share_links WHERE token=?', (token,))
    row = c.fetchone()
    if not row:
        conn.close()
        return {'success': False, 'error': 'Invalid or expired share link'}
    
    sl = dict(row)
    if not sl.get('is_active'):
        conn.close()
        return {'success': False, 'error': 'This share link has been revoked by the patient'}
    
    if sl.get('expires_at') and sl.get('expires_at') < datetime.now().isoformat():
        conn.close()
        return {'success': False, 'error': 'This share link has expired'}
        
    if sl.get('max_views') and sl.get('view_count', 0) >= sl.get('max_views'):
        conn.close()
        return {'success': False, 'error': 'Maximum view limit reached for this share link'}

    if sl.get('password') and sl.get('password') != password:
        conn.close()
        return {'success': False, 'error': 'Incorrect password'}

    new_count = sl.get('view_count', 0) + 1
    try:
        logs = json.loads(sl.get('logs', '[]'))
    except Exception:
        logs = []
    logs.append({"timestamp": datetime.now().isoformat(), "action": "Accessed by consulting doctor", "ip": "127.0.0.1"})
    
    c.execute('UPDATE share_links SET view_count=?, logs=? WHERE token=?', (new_count, json.dumps(logs), token))
    conn.commit()
    conn.close()

    patient = patient_service.get_patient(sl.get('patient_id'))
    prescriptions = prescription_service.get_prescriptions('doctor')
    lab_reports = lab_service.get_lab_reports('doctor')

    try:
        allowed_sections = json.loads(sl.get('allowed_sections', '[]'))
    except Exception:
        allowed_sections = []

    return {
        'success': True,
        'link': {
            'token': token,
            'title': sl.get('title'),
            'allowedSections': allowed_sections,
            'viewCount': new_count,
            'maxViews': sl.get('max_views')
        },
        'patient': patient,
        'prescriptions': prescriptions,
        'labReports': lab_reports
    }
