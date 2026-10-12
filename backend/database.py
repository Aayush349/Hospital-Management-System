"""
MediConnect HMS — Database & Service Facade (Backwards Compatibility)
Delegates all calls to domain-driven services in db/ and services/.
"""

from db.connection import get_db
from db import init_db
from config import LAB_PACKAGES
from services.department_service import (
    get_departments as api_get_departments,
    add_department as api_add_department,
    get_department_by_id as api_get_department_by_id,
    delete_department as api_delete_department
)
from services.doctor_service import (
    get_doctors as api_get_doctors,
    get_doctor_by_id as api_get_doctor_by_id,
    add_doctor as api_add_doctor,
    update_doctor as api_update_doctor,
    delete_doctor as api_delete_doctor
)
from services.patient_service import (
    get_patients as api_get_patients,
    get_patient as api_get_patient,
    add_patient as api_add_patient,
    update_patient as api_update_patient,
    delete_patient as api_delete_patient
)
from services.appointment_service import (
    get_appointments as api_get_appointments,
    get_appointment_by_id as api_get_appointment_by_id,
    create_appointment as api_create_appointment,
    update_appointment_status as api_update_appointment_status,
    delete_appointment as api_delete_appointment
)
from services.prescription_service import (
    get_prescriptions as api_get_prescriptions,
    get_prescription_by_id as api_get_prescription_by_id,
    create_prescription as api_create_prescription,
    delete_prescription as api_delete_prescription
)
from services.lab_service import (
    get_lab_reports as api_get_lab_reports,
    create_lab_report as api_create_lab_report,
    delete_lab_report as api_delete_lab_report,
    get_lab_packages as api_get_lab_packages,
    get_home_sample_orders as api_get_home_sample_orders,
    create_home_sample_order as api_create_home_sample_order,
    update_sample_order_status as api_update_sample_order_status
)
from services.share_link_service import (
    get_share_links as api_get_share_links,
    create_share_link as api_create_share_link,
    delete_share_link as api_delete_share_link,
    verify_share_link as api_verify_share_link
)
from services.auth_service import (
    login_user as api_login_user,
    register_user as api_register_user,
    reset_password as api_reset_password,
    get_users as api_get_users
)
from services.chat_service import (
    get_chat_history as api_get_chat_history,
    save_chat_message as api_save_chat_message,
    clear_chat_history as api_clear_chat_history,
    generate_ai_reply as api_generate_ai_reply
)
from services.admin_service import (
    get_admin_stats as api_get_admin_stats,
    get_cloud_status as api_get_cloud_status
)

__all__ = [
    "get_db",
    "init_db",
    "LAB_PACKAGES",
    "api_get_departments",
    "api_add_department",
    "api_get_doctors",
    "api_get_doctor_by_id",
    "api_add_doctor",
    "api_update_doctor",
    "api_get_patient",
    "api_update_patient",
    "api_get_appointments",
    "api_create_appointment",
    "api_update_appointment_status",
    "api_get_prescriptions",
    "api_create_prescription",
    "api_get_lab_reports",
    "api_create_lab_report",
    "api_get_lab_packages",
    "api_get_home_sample_orders",
    "api_create_home_sample_order",
    "api_update_sample_order_status",
    "api_get_share_links",
    "api_create_share_link",
    "api_delete_share_link",
    "api_verify_share_link",
    "api_login_user",
    "api_register_user",
    "api_reset_password",
    "api_get_users",
    "api_get_chat_history",
    "api_save_chat_message",
    "api_clear_chat_history"
]
