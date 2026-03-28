"""
Appointments API routes
"""
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db import models
from app.schemas.appointment import (
    AppointmentResponse,
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentStatus,
)
from app.core.logging import logger

router = APIRouter(
    prefix="/api/v1/appointments",
    tags=["appointments"],
)


@router.get("", response_model=List[AppointmentResponse])
async def list_appointments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List all appointments."""
    try:
        appointments = db.query(models.Appointment).offset(skip).limit(limit).all()
        return appointments
    except Exception as e:
        logger.error(f"Error listing appointments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch appointments",
        )


@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """Get a specific appointment."""
    try:
        appointment = db.query(models.Appointment).filter(
            models.Appointment.id == appointment_id
        ).first()
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found",
            )
        return appointment
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching appointment {appointment_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch appointment",
        )


@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
):
    """Create a new appointment."""
    try:
        db_appointment = models.Appointment(**appointment.dict())
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        logger.info(f"Appointment {db_appointment.id} created")
        return db_appointment
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating appointment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create appointment",
        )


@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    db: Session = Depends(get_db),
):
    """Update an appointment."""
    try:
        db_appointment = db.query(models.Appointment).filter(
            models.Appointment.id == appointment_id
        ).first()
        if not db_appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found",
            )
        
        update_data = appointment.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_appointment, field, value)
        
        db.commit()
        db.refresh(db_appointment)
        logger.info(f"Appointment {appointment_id} updated")
        return db_appointment
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating appointment {appointment_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update appointment",
        )


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
):
    """Delete (cancel) an appointment."""
    try:
        db_appointment = db.query(models.Appointment).filter(
            models.Appointment.id == appointment_id
        ).first()
        if not db_appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found",
            )
        
        db_appointment.status = models.AppointmentStatus.cancelled
        db.commit()
        logger.info(f"Appointment {appointment_id} cancelled")
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error cancelling appointment {appointment_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel appointment",
        )


__all__ = ["router"]
