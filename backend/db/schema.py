"""
MediConnect HMS — Database Schema
All CREATE TABLE statements. Called once at startup.
"""


def init_tables(conn):
    """Create all tables if they don't already exist."""
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT,
        username TEXT UNIQUE,
        role TEXT NOT NULL,
        password TEXT NOT NULL,
        security_pin TEXT DEFAULT '1234',
        created_at TEXT,
        assigned_doctor_id TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        code TEXT,
        icon TEXT,
        color TEXT,
        description TEXT,
        room TEXT,
        doctor_count INTEGER DEFAULT 1
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        department TEXT,
        specialization TEXT,
        experience INTEGER,
        qualification TEXT,
        room_no TEXT,
        fee INTEGER DEFAULT 500,
        available_days TEXT,
        image TEXT,
        about TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        uhid TEXT UNIQUE,
        age INTEGER,
        gender TEXT,
        blood_group TEXT,
        phone TEXT,
        email TEXT,
        abha_id TEXT,
        emergency_contact TEXT,
        address TEXT,
        allergies TEXT,
        chronic_conditions TEXT,
        security_pin TEXT DEFAULT '1234',
        privacy_settings TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id TEXT PRIMARY KEY,
        patient_id TEXT,
        patient_name TEXT,
        patient_age INTEGER,
        patient_gender TEXT,
        patient_phone TEXT,
        doctor_id TEXT,
        doctor_name TEXT,
        department TEXT,
        date TEXT,
        time TEXT,
        slot TEXT,
        status TEXT DEFAULT 'Scheduled',
        token_number TEXT,
        type TEXT DEFAULT 'In-Person',
        symptoms TEXT,
        history_summary TEXT,
        vitals TEXT,
        notes TEXT,
        created_at TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS prescriptions (
        id TEXT PRIMARY KEY,
        appointment_id TEXT,
        patient_id TEXT,
        patient_name TEXT,
        doctor_id TEXT,
        doctor_name TEXT,
        date TEXT,
        diagnosis TEXT,
        vitals TEXT,
        medicines TEXT,
        advice TEXT,
        follow_up TEXT,
        created_at TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS lab_reports (
        id TEXT PRIMARY KEY,
        patient_id TEXT,
        test_name TEXT,
        test_type TEXT,
        department TEXT,
        date TEXT,
        doctor_name TEXT,
        status TEXT,
        result TEXT,
        normal_range TEXT,
        unit TEXT,
        summary TEXT,
        file_name TEXT,
        file_url TEXT,
        created_at TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS sample_orders (
        id TEXT PRIMARY KEY,
        patient_id TEXT,
        patient_name TEXT,
        test_name TEXT,
        date TEXT,
        time_slot TEXT,
        address TEXT,
        phone TEXT,
        fee INTEGER DEFAULT 499,
        status TEXT DEFAULT 'requested',
        phlebotomist TEXT,
        timeline TEXT,
        created_at TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS share_links (
        id TEXT PRIMARY KEY,
        patient_id TEXT,
        token TEXT UNIQUE,
        title TEXT,
        expires_at TEXT,
        password TEXT,
        max_views INTEGER DEFAULT 5,
        view_count INTEGER DEFAULT 0,
        is_active INTEGER DEFAULT 1,
        allowed_sections TEXT,
        created_at TEXT,
        logs TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS chat_messages (
        id TEXT PRIMARY KEY,
        session_id TEXT,
        sender TEXT,
        message TEXT,
        role TEXT,
        timestamp TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS audit_logs (
        id TEXT PRIMARY KEY,
        action TEXT,
        user_role TEXT,
        user_name TEXT,
        target_id TEXT,
        timestamp TEXT,
        details TEXT
    )
    ''')

    conn.commit()
