"""
MediConnect HMS — Lab & Diagnostics Service
Business logic and persistence for lab reports, health packages, and home sample collections.
"""

import json
from datetime import datetime
from db.connection import get_db
from config import LAB_PACKAGES


def get_lab_reports(role='doctor'):
    """Fetch lab reports. Returns empty list for admin role to preserve clinical confidentiality."""
    if role == 'admin':
        return []

    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM lab_reports ORDER BY created_at DESC')
    rows = []
    for r in c.fetchall():
        lr = dict(r)
        lr['testName'] = lr.get('test_name')
        lr['testType'] = lr.get('test_type')
        lr['doctorName'] = lr.get('doctor_name')
        lr['normalRange'] = lr.get('normal_range')
        lr['fileName'] = lr.get('file_name')
        lr['fileUrl'] = lr.get('file_url')
        rows.append(lr)
    conn.close()
    return rows


def create_lab_report(data):
    """Save a new lab test report."""
    conn = get_db()
    c = conn.cursor()
    lr_id = data.get('id') or f"lab-{int(datetime.now().timestamp())}"
    now = datetime.now().isoformat()
    c.execute('''
    INSERT INTO lab_reports (id, patient_id, test_name, test_type, department, date, doctor_name,
                             status, result, normal_range, unit, summary, file_name, file_url, created_at)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        lr_id,
        data.get('patientId', 'pat-1'),
        data.get('testName'),
        data.get('testType', 'Biochemistry'),
        data.get('department', 'Pathology Lab'),
        data.get('date', datetime.now().strftime('%Y-%m-%d')),
        data.get('doctorName', 'Pathologist'),
        data.get('status', 'Completed'),
        data.get('result', ''),
        data.get('normalRange', ''),
        data.get('unit', ''),
        data.get('summary', ''),
        data.get('fileName', 'Report.pdf'),
        data.get('fileUrl', '#'),
        now
    ))
    conn.commit()
    result = dict(data)
    result['id'] = lr_id
    return result


def delete_lab_report(lr_id):
    """Delete a lab report by ID."""
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM lab_reports WHERE id=?', (lr_id,))
    conn.commit()
    conn.close()
    return {'success': True, 'id': lr_id}


def get_lab_packages():
    """Retrieve available lab checkup packages catalog."""
    return LAB_PACKAGES


def get_home_sample_orders(patient_id=None):
    """Fetch doorstep sample collection orders."""
    conn = get_db()
    c = conn.cursor()
    if patient_id:
        c.execute('SELECT * FROM sample_orders WHERE patient_id=? ORDER BY created_at DESC', (patient_id,))
    else:
        c.execute('SELECT * FROM sample_orders ORDER BY created_at DESC')
    rows = []
    for r in c.fetchall():
        o = dict(r)
        try:
            o['phlebotomist'] = json.loads(o.get('phlebotomist', '{}'))
        except Exception:
            o['phlebotomist'] = {}
        try:
            o['timeline'] = json.loads(o.get('timeline', '[]'))
        except Exception:
            o['timeline'] = []
        rows.append(o)
    conn.close()
    return rows


def create_home_sample_order(data):
    """Book a new home sample collection."""
    conn = get_db()
    c = conn.cursor()
    order_id = data.get('id') or f"HSL-{int(datetime.now().timestamp()) % 10000:04d}"
    phlebo = {
        'name': 'Ramesh Kumar',
        'phone': '+91 98112 84729',
        'rating': '4.9 ★',
        'badge': 'Vaccinated Specialist',
        'vehicle': 'MediConnect Sample Bike (DL 3S CK 4912)'
    }
    timeline = [
        {"step": "requested", "title": "Order Placed", "time": "Just now", "done": True, "current": True},
        {"step": "assigned", "title": "Phlebotomist Assigned", "time": "Pending", "done": False, "current": False},
        {"step": "collected", "title": "Sample Collection at Doorstep", "time": "Pending", "done": False, "current": False},
        {"step": "processing", "title": "Lab Testing & Quality Check", "time": "Pending", "done": False, "current": False},
        {"step": "ready", "title": "Digital Report Ready", "time": "Pending", "done": False, "current": False}
    ]
    now = datetime.now().isoformat()
    c.execute('''
    INSERT INTO sample_orders (id, patient_id, patient_name, test_name, date, time_slot, address, phone, fee, status, phlebotomist, timeline, created_at)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        order_id,
        data.get('patientId', 'pat-1'),
        data.get('patientName', 'Tushar Tawar'),
        data.get('testName', 'Full Body Checkup'),
        data.get('date', datetime.now().strftime('%Y-%m-%d')),
        data.get('timeSlot', '08:00 AM - 09:00 AM'),
        data.get('address', 'Home'),
        data.get('phone', '+91 98765 43210'),
        data.get('fee', 499),
        'requested',
        json.dumps(phlebo),
        json.dumps(timeline),
        now
    ))
    conn.commit()
    result = dict(data)
    result['id'] = order_id
    result['status'] = 'requested'
    result['phlebotomist'] = phlebo
    result['timeline'] = timeline
    return result


def update_sample_order_status(order_id, new_status):
    """Advance the home sample order through processing stages."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM sample_orders WHERE id=?', (order_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return None
    ord_dict = dict(row)
    try:
        timeline = json.loads(ord_dict.get('timeline', '[]'))
    except Exception:
        timeline = []
    
    steps = ['requested', 'assigned', 'collected', 'processing', 'ready']
    if new_status in steps:
        curr_idx = steps.index(new_status)
        for i, step in enumerate(timeline):
            step['done'] = i <= curr_idx
            step['current'] = i == curr_idx
            if i <= curr_idx and step.get('time') == 'Pending':
                step['time'] = 'Updated'
    
    c.execute('UPDATE sample_orders SET status=?, timeline=? WHERE id=?', (new_status, json.dumps(timeline), order_id))
    conn.commit()
    conn.close()
    ord_dict['status'] = new_status
    ord_dict['timeline'] = timeline
    return ord_dict
