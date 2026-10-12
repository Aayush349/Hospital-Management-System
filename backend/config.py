"""
MediConnect HMS — Application Configuration
Central constants, paths, and static catalog data.
"""

import os

try:
    from dotenv import load_dotenv
    # Check and load from backend/.env and root .env
    current_dir = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(current_dir, '.env'))
    load_dotenv(os.path.join(current_dir, '..', '.env'))
except ImportError:
    pass

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'mediconnect.db')
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend'))

# ── AI / OpenRouter Configuration ─────────────────────────────────────────────
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODELS = [
    "nvidia/nemotron-3.5-lightning:free",
    "google/gemma-4-26b-a4b-it:free",
    "google/gemma-4-31b-it:free",
    "liquid/lfm-2.5-2.6b:free"
]

# ── Static Catalog: Lab Packages ──────────────────────────────────────────────
LAB_PACKAGES = [
    {
        "id": "pkg-1",
        "name": "Comprehensive Full Body Health Checkup",
        "tag": "Most Popular",
        "badgeColor": "teal",
        "testsCount": 84,
        "sampleType": "Blood & Urine",
        "fastingRequired": "10-12 hours fasting required",
        "turnaroundHours": 24,
        "originalPrice": 2499,
        "price": 999,
        "discount": "60% OFF",
        "parameters": [
            "Complete Hemogram (28 tests)", "Lipid Profile (8 tests)",
            "Liver Function Test - LFT (12 tests)", "Kidney Function Test - KFT (8 tests)",
            "Thyroid Profile Total (3 tests)", "Fasting Blood Sugar (HbA1c)",
            "Vitamin D Total & Vitamin B12", "Urine Routine Examination (20 tests)"
        ]
    },
    {
        "id": "pkg-2",
        "name": "Advanced Heart Care & Cardiac Risk Panel",
        "tag": "Doctor Recommended",
        "badgeColor": "rose",
        "testsCount": 42,
        "sampleType": "Blood",
        "fastingRequired": "12 hours fasting required",
        "turnaroundHours": 18,
        "originalPrice": 3200,
        "price": 1499,
        "discount": "53% OFF",
        "parameters": [
            "High Sensitivity CRP (hs-CRP)", "Apolipoprotein A1 & B",
            "Lipid Extended Panel with Ratios", "Homocysteine Quantitative",
            "Serum Electrolytes (Na, K, Cl)", "Creatine Kinase (CK-MB)"
        ]
    },
    {
        "id": "pkg-3",
        "name": "Senior Citizen Vital Care Package",
        "tag": "Specialized",
        "badgeColor": "indigo",
        "testsCount": 65,
        "sampleType": "Blood & Urine",
        "fastingRequired": "10 hours fasting required",
        "turnaroundHours": 24,
        "originalPrice": 3800,
        "price": 1699,
        "discount": "55% OFF",
        "parameters": [
            "Bone Mineral Density (Calcium, Phosphorus)", "Rheumatoid Factor (RA Factor)",
            "Complete Renal Profile with eGFR", "Serum Uric Acid",
            "Iron Deficiency Profile with Ferritin", "HbA1c Glycated Hemoglobin"
        ]
    }
]
