"""
MediConnect HMS — Services Package
Exposes domain-driven services decoupling business logic from HTTP transport routers.
"""

from services import (
    auth_service,
    patient_service,
    doctor_service,
    appointment_service,
    prescription_service,
    lab_service,
    department_service,
    admin_service,
    share_link_service,
    chat_service
)

__all__ = [
    "auth_service",
    "patient_service",
    "doctor_service",
    "appointment_service",
    "prescription_service",
    "lab_service",
    "department_service",
    "admin_service",
    "share_link_service",
    "chat_service"
]
