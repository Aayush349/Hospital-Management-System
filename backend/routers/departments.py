from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, List
from models.department import DepartmentCreate, DepartmentUpdate
from services import department_service

router = APIRouter(prefix="/api/departments", tags=["Departments"])


@router.get("", response_model=List[Dict[str, Any]])
def get_departments():
    return department_service.get_departments()


@router.get("/{dept_id}")
def get_department(dept_id: str):
    dept = department_service.get_department_by_id(dept_id)
    if not dept:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return dept


@router.post("", status_code=status.HTTP_201_CREATED)
def add_department(payload: DepartmentCreate):
    return department_service.add_department(payload.dict())


@router.put("/{dept_id}")
def update_department(dept_id: str, payload: DepartmentUpdate):
    updated = department_service.update_department(dept_id, payload.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return updated


@router.delete("/{dept_id}")
def delete_department(dept_id: str):
    return department_service.delete_department(dept_id)
