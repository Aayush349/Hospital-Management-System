"""
MediConnect HMS — Department Service
Business logic and persistence for hospital departments.
"""

from datetime import datetime
from db.connection import get_db


def get_departments():
    """Fetch all departments."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM departments')
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_department_by_id(dept_id):
    """Fetch a single department by ID."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM departments WHERE id=?', (dept_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def add_department(data):
    """Create a new hospital department."""
    conn = get_db()
    c = conn.cursor()
    dept_id = data.get('id') or f"dept-{int(datetime.now().timestamp())}"
    c.execute('''
    INSERT INTO departments (id, name, code, icon, color, description, room, doctor_count)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        dept_id,
        data.get('name'),
        data.get('code', 'GEN'),
        data.get('icon', 'Building'),
        data.get('color', 'teal'),
        data.get('description', ''),
        data.get('room', 'Block A'),
        data.get('doctorCount', 1)
    ))
    conn.commit()
    conn.close()
    result = dict(data)
    result['id'] = dept_id
    return result


def update_department(dept_id, data):
    """Update department information."""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
    UPDATE departments SET name=COALESCE(?, name), code=COALESCE(?, code),
                           icon=COALESCE(?, icon), color=COALESCE(?, color),
                           description=COALESCE(?, description), room=COALESCE(?, room),
                           doctor_count=COALESCE(?, doctor_count)
    WHERE id=?
    ''', (
        data.get('name'),
        data.get('code'),
        data.get('icon'),
        data.get('color'),
        data.get('description'),
        data.get('room'),
        data.get('doctorCount'),
        dept_id
    ))
    conn.commit()
    conn.close()
    return get_department_by_id(dept_id)


def delete_department(dept_id):
    """Delete a department by ID."""
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM departments WHERE id=?', (dept_id,))
    conn.commit()
    conn.close()
    return {'success': True, 'id': dept_id}
