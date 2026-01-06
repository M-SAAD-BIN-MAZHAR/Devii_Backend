from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth.dependencies import get_current_ambassador
from app.crud.payment import verify_cash_payment
from app.crud.participant import search_participants
from app.schemas.payment import PaymentVerification

router = APIRouter()

@router.get("/search")
def search_participant(
    email: str = None,
    student_id: str = None,
    db: Session = Depends(get_db),
    ambassador = Depends(get_current_ambassador)
):
    if not email and not student_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide either email or student_id"
        )
    
    participants = search_participants(db, email=email, student_id=student_id)
    return participants

@router.post("/verify-cash")
def verify_cash(
    verification: PaymentVerification,
    db: Session = Depends(get_db),
    ambassador = Depends(get_current_ambassador)
):
    payment = verify_cash_payment(
        db=db,
        participant_id=verification.participant_id,
        ambassador_id=ambassador.id
    )
    
     
    
    return {"message": "Payment verified successfully", "payment_id": payment.id}