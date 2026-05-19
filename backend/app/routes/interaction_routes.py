from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Interaction, HCP, FollowUp
from app.schemas.schemas import (
    InteractionCreate, InteractionResponse, InteractionUpdate, FollowUpCreate, FollowUpResponse
)
from datetime import datetime

router = APIRouter(prefix="/api/interactions", tags=["Interactions"])

@router.post("/", response_model=InteractionResponse)
def create_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    """Create a new interaction"""
    # Verify HCP exists
    hcp = db.query(HCP).filter(HCP.id == interaction.hcp_id).first()
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    
    db_interaction = Interaction(**interaction.dict())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

@router.get("/{interaction_id}", response_model=InteractionResponse)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Get interaction by ID"""
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction

@router.get("/hcp/{hcp_id}", response_model=list[InteractionResponse])
def get_hcp_interactions(hcp_id: int, db: Session = Depends(get_db)):
    """Get all interactions for an HCP"""
    return db.query(Interaction).filter(Interaction.hcp_id == hcp_id).all()

@router.get("/", response_model=list[InteractionResponse])
def list_interactions(db: Session = Depends(get_db)):
    """List all interactions"""
    return db.query(Interaction).all()

@router.put("/{interaction_id}", response_model=InteractionResponse)
def update_interaction(interaction_id: int, interaction: InteractionUpdate, db: Session = Depends(get_db)):
    """Update interaction"""
    db_interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not db_interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    update_data = interaction.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_interaction, field, value)
    
    db_interaction.updated_at = datetime.utcnow()
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

@router.delete("/{interaction_id}")
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Delete interaction"""
    db_interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not db_interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    db.delete(db_interaction)
    db.commit()
    return {"detail": "Interaction deleted successfully"}

@router.post("/{interaction_id}/follow-ups/", response_model=FollowUpResponse)
def create_follow_up(interaction_id: int, follow_up: FollowUpCreate, db: Session = Depends(get_db)):
    """Create follow-up for an interaction"""
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    db_follow_up = FollowUp(
        interaction_id=interaction_id,
        action_item=follow_up.action_item,
        due_date=follow_up.due_date,
        completed=follow_up.completed
    )
    db.add(db_follow_up)
    db.commit()
    db.refresh(db_follow_up)
    return db_follow_up

@router.get("/{interaction_id}/follow-ups/", response_model=list[FollowUpResponse])
def get_follow_ups(interaction_id: int, db: Session = Depends(get_db)):
    """Get follow-ups for an interaction"""
    return db.query(FollowUp).filter(FollowUp.interaction_id == interaction_id).all()
