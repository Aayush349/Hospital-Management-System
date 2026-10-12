"""
MediConnect HMS — Authentication & User Management Service
Handles multi-role logins, account signups, security PIN validation, and password resets.
"""

import json
import sqlite3
from datetime import datetime
from db.connection import get_db


def login_user(identifier, password, role):
    """Authenticate user credentials matching email, phone, or username for a given role."""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
    SELECT * FROM users 
    WHERE (email=? OR phone=? OR username=?) AND role=?
    ''', (identifier, identifier, identifier, role))
    user = c.fetchone()
    conn.close()

    if not user:
        return {'success': False, 'error': f'No {role} account found matching "{identifier}".'}
    
    u = dict(user)
    if u.get('password') != password:
        return {'success': False, 'error': 'Incorrect password. Please verify and try again.'}

    return {
        'success': True,
        'user': {
            'id': u.get('id'),
            'name': u.get('name'),
            'email': u.get('email'),
            'phone': u.get('phone'),
            'username': u.get('username'),
            'role': u.get('role'),
            'securityPin': u.get('security_pin'),
            'assignedDoctorId': u.get('assigned_doctor_id')
        }
    }


def register_user(data):
    """Register a new user account and initialize profile records."""
    if data.get('role') == 'admin':
        return {'success': False, 'error': 'Registration for Hospital Administrator is permanently disabled for security.'}

    conn = get_db()
    c = conn.cursor()
    
    email = data.get('email')
    phone = data.get('phone')
    username = email.split('@')[0] if email else f"user_{int(datetime.now().timestamp())}"
    user_id = f"usr-{data.get('role', 'patient')[:3]}-{int(datetime.now().timestamp())}"
    pin = data.get('securityPin') or '1234'
    now = datetime.now().isoformat()

    try:
        c.execute('''
        INSERT INTO users (id, name, email, phone, username, role, password, security_pin, created_at, assigned_doctor_id)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        ''', (
            user_id,
            data.get('name'),
            email,
            phone,
            username,
            data.get('role', 'patient'),
            data.get('password'),
            pin,
            now,
            data.get('assignedDoctorId')
        ))
        
        if data.get('role') == 'patient':
            pat_id = f"pat-{int(datetime.now().timestamp())}"
            uhid = f"MC-2026-{int(datetime.now().timestamp()) % 10000:04d}"
            privacy = json.dumps({"block_admin_clinical": True, "require_doctor_consent_pin": True})
            c.execute('''
            INSERT INTO patients (id, name, uhid, age, gender, blood_group, phone, email, abha_id, emergency_contact, address, allergies, chronic_conditions, security_pin, privacy_settings)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (
                pat_id,
                data.get('name'),
                uhid,
                28,
                'Male',
                'B+',
                phone,
                email,
                '',
                '',
                'India',
                '[]',
                '[]',
                pin,
                privacy
            ))

        conn.commit()
        conn.close()
        return {
            'success': True,
            'user': {
                'id': user_id,
                'name': data.get('name'),
                'email': email,
                'role': data.get('role'),
                'securityPin': pin,
                'assignedDoctorId': data.get('assignedDoctorId')
            }
        }
    except sqlite3.IntegrityError:
        conn.close()
        return {'success': False, 'error': 'An account with this email or phone number already exists.'}
    except Exception as e:
        conn.close()
        return {'success': False, 'error': str(e)}


def reset_password(identifier, security_pin, new_pass):
    """Reset user password after verifying security PIN."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email=? OR phone=? OR username=?', (identifier, identifier, identifier))
    user = c.fetchone()
    if not user:
        conn.close()
        return {'success': False, 'error': f'No user found for "{identifier}".'}
    
    u = dict(user)
    if u.get('security_pin') and security_pin and u.get('security_pin') != security_pin.strip():
        conn.close()
        return {'success': False, 'error': 'Invalid 4-digit Security Key.'}

    c.execute('UPDATE users SET password=? WHERE id=?', (new_pass, u.get('id')))
    conn.commit()
    conn.close()
    return {'success': True, 'message': 'Password reset successfully! You can now login.'}


def get_users():
    """Retrieve all users in the system."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    rows = c.fetchall()
    conn.close()
    users = []
    for r in rows:
        u = dict(r)
        if 'assigned_doctor_id' in u:
            u['assignedDoctorId'] = u['assigned_doctor_id']
        users.append(u)
    return users
