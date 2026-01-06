from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from io import BytesIO
from fastapi.responses import StreamingResponse
from app.database import get_db
from app.auth.dependencies import get_current_admin
from app.crud.user import get_all_users, update_user_role
from app.crud.participant import get_all_participants
from app.crud.payment import get_payments_summary, verify_online_payment
from app.schemas.user import UserRole

router = APIRouter()

@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    summary = {
        "total_participants": get_all_participants(db).count(),
        "payments_summary": get_payments_summary(db),
        "track_distribution": get_track_distribution(db),
        "university_distribution": get_university_distribution(db)
    }
    return summary

@router.post("/verify-payment/{payment_id}")
def verify_payment_admin(
    payment_id: int,
    approve: bool = True,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    payment = verify_online_payment(db, payment_id, approve)
    
    if approve:
        # Generate and send QR code
        # TODO: Implement QR generation
        pass
    
    return {"message": f"Payment {'approved' if approve else 'rejected'}", "payment_id": payment.id}

@router.get("/export")
def export_registrations(
    format: str = "csv",
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    participants = get_all_participants(db).all()
    
    # Convert to DataFrame
    data = []
    for p in participants:
        data.append({
            "Full Name": p.user.full_name,
            "Email": p.user.email,
            "University": p.user.university,
            "Track": p.track,
            "Team": p.team.name if p.team else "Individual",
            "Payment Status": p.payment.status if p.payment else "No Payment"
        })
    
    df = pd.DataFrame(data)
    
    if format == "excel":
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Registrations')
        output.seek(0)
        
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=devcon26_registrations.xlsx"}
        )
    else:
        csv_data = df.to_csv(index=False)
        return StreamingResponse(
            iter([csv_data]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=devcon26_registrations.csv"}
        )