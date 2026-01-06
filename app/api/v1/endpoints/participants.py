from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
from app.database import get_db
from app.auth.dependencies import get_current_participant, get_current_user
from app.schemas.participant import ParticipantCreate, ParticipantInDB
from app.schemas.payment import PaymentCreate, PaymentInDB
from app.crud.participant import create_participant,get_participant_by_user_id
from app.crud.team import create_team, join_team
from app.crud.payment import create_payment
from app.config import settings
from app.utils.validators import validate_file_upload

router = APIRouter()

@router.post("/register", response_model=ParticipantInDB)
def register_participant(
    participant_data: ParticipantCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if user already has a participant profile
    existing = get_participant_by_user_id(db, current_user.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Participant profile already exists"
        )
    
    # Create participant
    participant = create_participant(db, participant_data, current_user.id)
    
    # Handle team creation/joining
    if participant_data.create_new_team and participant_data.team_name:
        team = create_team(
            db, 
            participant_data.team_name, 
            participant.track,
            participant.id
        )
        participant.team_id = team.id
        participant.is_team_lead = True
    elif participant_data.team_code:
        team = join_team(db, participant_data.team_code, participant.id)
        participant.team_id = team.id
    
    db.commit()
    db.refresh(participant)
    return participant

@router.post("/payment/online")
def upload_payment_proof(
    payment_data: PaymentCreate,
    receipt: UploadFile = File(...),
    current_participant = Depends(get_current_participant),
    db: Session = Depends(get_db)
):
    # Validate file
    validate_file_upload(receipt, settings.ALLOWED_EXTENSIONS, settings.MAX_FILE_SIZE)
    
    # Save file
    file_path = os.path.join(settings.UPLOAD_DIR, f"receipt_{current_participant.id}_{receipt.filename}")
    with open(file_path, "wb") as buffer:
        content = receipt.file.read()
        buffer.write(content)
    
    # Create payment record
    payment = create_payment(
        db=db,
        participant_id=current_participant.id,
        team_id=current_participant.team_id,
        amount=settings.REGISTRATION_FEE,
        payment_method="online",
        transaction_id=payment_data.transaction_id,
        receipt_path=file_path
    )
    
    # Send confirmation email (async)
    # TODO: Implement email sending
    
    return {"message": "Payment proof uploaded successfully", "payment_id": payment.id}