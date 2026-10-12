from typing import Optional
from pydantic import BaseModel


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
