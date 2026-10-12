"""
MediConnect HMS — Database Seed Data
Populates default data if tables are empty.
"""

import json
from datetime import datetime


def seed_data_if_empty(conn):
    """Seed default records for users, departments, doctors, patients, appointments, etc."""
    c = conn.cursor()

    # 1. Users Seed
    c.execute('SELECT COUNT(*) FROM users')
    if c.fetchone()[0] == 0:
        now = datetime.now().isoformat()
        users = [
            ('usr-pat-1', 'Tushar Tawar', 'tushar.tawar@example.com', '+91 98765 43210', 'tushar.tawar', 'patient', 'patient123', '1234', now, None),
            ('usr-doc-1', 'Dr. Ananya Sharma', 'dr.ananya@mediconnect.in', '+91 98111 88888', 'dr.ananya', 'doctor', 'doctor123', '4321', now, 'doc-1'),
            ('usr-doc-2', 'Dr. Rajesh Verma', 'dr.rajesh@mediconnect.in', '+91 98222 77777', 'dr.rajesh', 'doctor', 'doctor123', '4321', now, 'doc-2'),
            ('usr-adm-1', 'Hospital IT Administration', 'admin@mediconnect.in', '+91 98999 00000', 'admin', 'admin', 'admin@hms', '9999', now, None),
            ('usr-rec-1', 'Reception Desk', 'receptionist@mediconnect.in', '+91 98777 66666', 'receptionist', 'receptionist', 'desk123', '7777', now, 'doc-1')
        ]
        c.executemany('INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?)', users)

    # 2. Departments Seed
    c.execute('SELECT COUNT(*) FROM departments')
    if c.fetchone()[0] == 0:
        depts = [
            ('dept-1', 'Cardiology', 'CARD', 'HeartPulse', 'rose', 'Advanced cardiac catheterization, arrhythmia treatment, non-invasive imaging, and angioplasty.', 'Room 201, Block B', 3),
            ('dept-2', 'Neurology', 'NEUR', 'Brain', 'purple', 'Comprehensive stroke management, epilepsy diagnostics, neuro-electrophysiology, and Parkinson care.', 'Room 305, Block A', 2),
            ('dept-3', 'Orthopedics', 'ORTH', 'Bone', 'amber', 'Robotic joint replacement, sports injury arthroscopy, spine surgery, and trauma management.', 'Room 110, Ground Floor', 4),
            ('dept-4', 'General Medicine', 'GEN', 'Stethoscope', 'teal', 'Primary preventative care, acute infectious disease management, and chronic multi-system treatment.', 'Room 102, Ground Floor', 5),
            ('dept-5', 'Pediatrics', 'PED', 'Baby', 'sky', 'Neonatal intensive care (NICU level 3), child immunizations, and developmental monitoring.', 'Room 214, Block C', 3),
            ('dept-6', 'Dermatology', 'DERM', 'Activity', 'pink', 'Phototherapy, skin biopsy analysis, autoimmune dermatoses, and cosmetic laser treatments.', 'Room 402, Block A', 2)
        ]
        c.executemany('INSERT INTO departments VALUES (?,?,?,?,?,?,?,?)', depts)

    # 3. Doctors Seed
    c.execute('SELECT COUNT(*) FROM doctors')
    if c.fetchone()[0] == 0:
        doctors = [
            ('doc-1', 'Dr. Ananya Sharma', 'dr.ananya@mediconnect.in', '+91 98111 88888', 'Cardiology', 'Senior Interventional Cardiologist', 14, 'MBBS, MD (Med), DM (Cardio), FACC', 'Room 201', 800, json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri']), 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&q=80&w=300', 'Specializes in coronary interventions, acute coronary syndromes, and preventative heart care with 14+ years of clinical excellence.'),
            ('doc-2', 'Dr. Rajesh Verma', 'dr.rajesh@mediconnect.in', '+91 98222 77777', 'Neurology', 'Senior Consultant Neurosurgeon', 18, 'MBBS, MS (Gen Surg), MCh (Neurosurg)', 'Room 305', 1000, json.dumps(['Mon', 'Wed', 'Fri', 'Sat']), 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&q=80&w=300', 'Pioneer in minimally invasive keyhole neurosurgery and computer-assisted stereotactic brain surgery.'),
            ('doc-3', 'Dr. Vikram Malhotra', 'dr.vikram@mediconnect.in', '+91 98333 66666', 'Orthopedics', 'Lead Robotic Joint Replacement Surgeon', 12, 'MBBS, MS (Ortho), Fellowship in Arthroscopy (Germany)', 'Room 110', 700, json.dumps(['Tue', 'Thu', 'Fri', 'Sat']), 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?auto=format&fit=crop&q=80&w=300', 'Has performed over 3,200 successful robotic knee and hip arthroplasties.'),
            ('doc-4', 'Dr. Sunita Rao', 'dr.sunita@mediconnect.in', '+91 98444 55555', 'General Medicine', 'Chief Consultant Physician', 16, 'MBBS, MD (Internal Medicine)', 'Room 102', 600, json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']), 'https://images.unsplash.com/photo-1594824813511-20926d24a919?auto=format&fit=crop&q=80&w=300', 'Specializes in complex adult multi-morbidity, diabetes metabolic disorders, and geriatric health.')
        ]
        c.executemany('INSERT INTO doctors VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', doctors)

    # 4. Patient Seed
    c.execute('SELECT COUNT(*) FROM patients')
    if c.fetchone()[0] == 0:
        privacy_defaults = json.dumps({
            "block_admin_clinical": True,
            "require_doctor_consent_pin": True,
            "allow_treating_doctor_session": True,
            "notify_on_record_access": True
        })
        patient = (
            'pat-1',
            'Tushar Tawar',
            'MC-2025-08912',
            32,
            'Male',
            'O+',
            '+91 98765 43210',
            'tushar.tawar@example.com',
            '91-4432-8819-2041',
            'Pooja Tawar (Spouse: +91 98765 43219)',
            'Tower 4, Flat 702, DLF Phase 5, Gurugram, Haryana',
            json.dumps(['Penicillin', 'Sulfa Drugs']),
            json.dumps(['Mild Hypertension (Stage 1)']),
            '1234',
            privacy_defaults
        )
        c.execute('INSERT INTO patients VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', patient)

    # 5. Appointments Seed
    c.execute('SELECT COUNT(*) FROM appointments')
    if c.fetchone()[0] == 0:
        now_date = datetime.now().strftime('%Y-%m-%d')
        appts = [
            (
                'apt-1', 'pat-1', 'Tushar Tawar', 32, 'Male', '+91 98765 43210',
                'doc-1', 'Dr. Ananya Sharma', 'Cardiology',
                now_date, '10:30 AM', '10:30 AM - 10:45 AM', 'Scheduled', 'C-101', 'In-Person',
                'Mild exertional chest heaviness, recurrent palpitation after coffee',
                'Known hypertensive on ACE inhibitors for 2 years. Regular follow-up.',
                json.dumps({'bp': '128/84 mmHg', 'pulse': '76 bpm', 'spo2': '99%', 'temp': '98.6 F'}),
                'Routine quarterly cardiology review and resting ECG evaluation',
                datetime.now().isoformat()
            ),
            (
                'apt-2', 'pat-1', 'Tushar Tawar', 32, 'Male', '+91 98765 43210',
                'doc-4', 'Dr. Sunita Rao', 'General Medicine',
                '2026-09-18', '04:00 PM', '04:00 PM - 04:15 PM', 'Completed', 'G-042', 'In-Person',
                'Routine annual executive health wellness checkup and blood panel review',
                'Hypertension controlled. Normal BMI.',
                json.dumps({'bp': '124/80 mmHg', 'pulse': '72 bpm', 'spo2': '99%', 'temp': '98.4 F'}),
                'Vitals stable. Fasting blood profile advised.',
                datetime.now().isoformat()
            )
        ]
        c.executemany('INSERT INTO appointments VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', appts)

    # 6. Prescriptions Seed
    c.execute('SELECT COUNT(*) FROM prescriptions')
    if c.fetchone()[0] == 0:
        medicines = json.dumps([
            {"name": "Telmisartan 40mg", "dosage": "1 tablet OD", "duration": "30 days", "timing": "Morning after breakfast", "instructions": "Continue blood pressure maintenance"},
            {"name": "Atorvastatin 10mg", "dosage": "1 tablet HS", "duration": "30 days", "timing": "Night after dinner", "instructions": "Cardio-protective lipid optimization"}
        ])
        vitals = json.dumps({'bp': '126/82 mmHg', 'pulse': '74 bpm', 'weight': '72 kg'})
        rx = (
            'rx-1', 'apt-2', 'pat-1', 'Tushar Tawar',
            'doc-4', 'Dr. Sunita Rao', '2026-09-18',
            'Essential Primary Hypertension (Controlled)',
            vitals, medicines,
            'Low sodium diet (<2g/day). 30 mins brisk morning walk 5 days a week. Hydrate adequately.',
            'Follow up after 3 months with Lipid profile and Serum Creatinine.',
            datetime.now().isoformat()
        )
        c.execute('INSERT INTO prescriptions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', rx)

    # 7. Lab Reports Seed
    c.execute('SELECT COUNT(*) FROM lab_reports')
    if c.fetchone()[0] == 0:
        reports = [
            (
                'lab-1', 'pat-1', 'Comprehensive Lipid Profile', 'Blood Biochemistry', 'Biochemistry Lab 1',
                '2026-09-19', 'Dr. Sunita Rao', 'Completed', 'Total Chol: 182 mg/dL, HDL: 48, LDL: 110, Triglycerides: 140',
                'Desirable < 200 mg/dL', 'mg/dL', 'Normal lipid spectrum. Cardioprotective ratios within target.',
                'Lipid_Profile_Report_MC08912.pdf', '#', datetime.now().isoformat()
            ),
            (
                'lab-2', 'pat-1', '12-Lead Digital Resting ECG', 'Cardiovascular Diagnostics', 'Cardio Lab 2',
                '2026-09-20', 'Dr. Ananya Sharma', 'Completed', 'Normal Sinus Rhythm, HR 74 bpm, No ST-T segment elevation',
                'Normal Sinus Rhythm', 'bpm', 'Resting electrical heart activity within normal biological limits.',
                'ECG_12Lead_MC08912.pdf', '#', datetime.now().isoformat()
            )
        ]
        c.executemany('INSERT INTO lab_reports VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', reports)

    # 8. Share Links Seed
    c.execute('SELECT COUNT(*) FROM share_links')
    if c.fetchone()[0] == 0:
        share = (
            'link-1', 'pat-1', 'MEDIC-DELHI-7721', 'Pan-India Second Opinion Access Link',
            '2026-10-01T23:59:59', 'delhi2026', 10, 1, 1,
            json.dumps(['prescriptions', 'lab_reports', 'vitals', 'conditions']),
            datetime.now().isoformat(),
            json.dumps([{"timestamp": datetime.now().isoformat(), "ip": "127.0.0.1", "action": "Link created by patient"}])
        )
        c.execute('INSERT INTO share_links VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', share)

    conn.commit()
