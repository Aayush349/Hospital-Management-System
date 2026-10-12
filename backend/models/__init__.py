"""
MediConnect HMS — Pydantic Request & Response Schemas
"""

from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field


# ── Auth Models ───────────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    identifier: str
    password: str
    role: str = "patient"


class SignupRequest(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    password: str
    role: str = "patient"
    securityPin: Optional[str] = "1234"
    assignedDoctorId: Optional[str] = None


class ForgotPasswordRequest(BaseModel):
    identifier: str
    otp: Optional[str] = None
    securityPin: Optional[str] = "1234"
    newPassword: str


# ── Department Models ─────────────────────────────────────────────────────────
class DepartmentCreate(BaseModel):
    id: Optional[str] = None
    name: str
    code: Optional[str] = "GEN"
    icon: Optional[str] = "Building"
    color: Optional[str] = "teal"
    description: Optional[str] = ""
    room: Optional[str] = "Block A"
    doctorCount: Optional[int] = 1


# ── Doctor Models ─────────────────────────────────────────────────────────────
class DoctorCreate(BaseModel):
    id: Optional[str] = None
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    department: str
    specialization: Optional[str] = ""
    experience: Optional[int] = 5
    qualification: Optional[str] = ""
    roomNo: Optional[str] = "Room 101"
    fee: Optional[int] = 500
    availableDays: Optional[List[str]] = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    image: Optional[str] = None
    about: Optional[str] = ""


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    specialization: Optional[str] = None
    experience: Optional[int] = None
    qualification: Optional[str] = None
    roomNo: Optional[str] = None
    fee: Optional[int] = None
    availableDays: Optional[List[str]] = None
    image: Optional[str] = None
    about: Optional[str] = None


# ── Patient Models ────────────────────────────────────────────────────────────
class PatientCreate(BaseModel):
    id: Optional[str] = None
    name: str
    age: Optional[int] = 30
    gender: Optional[str] = "Male"
    bloodGroup: Optional[str] = "O+"
    phone: Optional[str] = None
    email: Optional[str] = None
    emergencyContact: Optional[str] = None
    address: Optional[str] = None
    allergies: Optional[Union[List[str], str]] = []
    chronicConditions: Optional[Union[List[str], str]] = []
    securityPin: Optional[str] = "1234"
    privacySettings: Optional[Dict[str, Any]] = {}


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    bloodGroup: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    emergencyContact: Optional[str] = None
    address: Optional[str] = None
    allergies: Optional[Union[List[str], str]] = None
    chronicConditions: Optional[Union[List[str], str]] = None
    securityPin: Optional[str] = None
    privacySettings: Optional[Dict[str, Any]] = None


# ── Appointment Models ────────────────────────────────────────────────────────
class AppointmentCreate(BaseModel):
    id: Optional[str] = None
    patientId: Optional[str] = "pat-1"
    patientName: Optional[str] = "Tushar Tawar"
    patientAge: Optional[int] = 32
    patientGender: Optional[str] = "Male"
    patientPhone: Optional[str] = "+91 98765 43210"
    doctorId: Optional[str] = None
    doctorName: Optional[str] = None
    department: Optional[str] = None
    doctorSpecialty: Optional[str] = None
    specialty: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = "10:00 AM"
    slot: Optional[str] = None
    timeSlot: Optional[str] = None
    status: Optional[str] = "Scheduled"
    tokenNumber: Optional[str] = None
    type: Optional[str] = "In-Person"
    symptoms: Optional[str] = ""
    historySummary: Optional[str] = ""
    vitals: Optional[Dict[str, Any]] = {}
    notes: Optional[str] = ""


class StatusUpdate(BaseModel):
    status: str


# ── Prescription Models ───────────────────────────────────────────────────────
class PrescriptionCreate(BaseModel):
    id: Optional[str] = None
    appointmentId: Optional[str] = None
    patientId: Optional[str] = "pat-1"
    patientName: Optional[str] = "Tushar Tawar"
    doctorId: Optional[str] = None
    doctorName: Optional[str] = None
    date: Optional[str] = None
    diagnosis: Optional[str] = None
    vitals: Optional[Dict[str, Any]] = {}
    medicines: Optional[List[Dict[str, Any]]] = []
    advice: Optional[str] = None
    followUp: Optional[str] = None


# ── Lab Models ────────────────────────────────────────────────────────────────
class LabReportCreate(BaseModel):
    id: Optional[str] = None
    patientId: Optional[str] = "pat-1"
    testName: str
    testType: Optional[str] = "Biochemistry"
    department: Optional[str] = "Pathology Lab"
    date: Optional[str] = None
    doctorName: Optional[str] = "Pathologist"
    status: Optional[str] = "Completed"
    result: Optional[str] = ""
    normalRange: Optional[str] = ""
    unit: Optional[str] = ""
    summary: Optional[str] = ""
    fileName: Optional[str] = "Report.pdf"
    fileUrl: Optional[str] = "#"


class SampleOrderCreate(BaseModel):
    id: Optional[str] = None
    patientId: Optional[str] = "pat-1"
    patientName: Optional[str] = "Tushar Tawar"
    testName: Optional[str] = "Full Body Checkup"
    date: Optional[str] = None
    timeSlot: Optional[str] = "08:00 AM - 09:00 AM"
    address: Optional[str] = "Home"
    phone: Optional[str] = "+91 98765 43210"
    fee: Optional[int] = 499


class OrderStatusUpdate(BaseModel):
    status: str


# ── Share Link Models ─────────────────────────────────────────────────────────
class ShareLinkCreate(BaseModel):
    id: Optional[str] = None
    patientId: Optional[str] = "pat-1"
    token: Optional[str] = None
    title: Optional[str] = "Doctor Consultation Share Link"
    expiresAt: Optional[str] = None
    password: Optional[str] = None
    maxViews: Optional[int] = 5
    allowedSections: Optional[List[str]] = ['prescriptions', 'lab_reports', 'vitals', 'conditions']


class VerifyRequest(BaseModel):
    token: str
    password: Optional[str] = ""


# ── Chat Models ───────────────────────────────────────────────────────────────
class ChatMessagePayload(BaseModel):
    sessionId: str
    sender: str
    message: str
    role: Optional[str] = "patient"


class ChatAskRequest(BaseModel):
    sessionId: Optional[str] = None
    message: str
    context: Optional[Dict[str, Any]] = None
