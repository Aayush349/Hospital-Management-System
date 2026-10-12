from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel


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
