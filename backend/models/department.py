from typing import Optional
from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    id: Optional[str] = None
    name: str
    code: Optional[str] = "GEN"
    icon: Optional[str] = "Building"
    color: Optional[str] = "teal"
    description: Optional[str] = ""
    room: Optional[str] = "Block A"
    doctorCount: Optional[int] = 1


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    room: Optional[str] = None
    doctorCount: Optional[int] = None
