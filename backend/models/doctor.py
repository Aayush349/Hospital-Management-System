from typing import Optional, List
from pydantic import BaseModel


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
