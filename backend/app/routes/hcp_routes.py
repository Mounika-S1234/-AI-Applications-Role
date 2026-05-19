from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import HCP, Interaction, FollowUp
from app.schemas.schemas import HCPCreate, HCPResponse, HCPUpdate, InteractionCreate, InteractionResponse, InteractionUpdate
from datetime import datetime

router = APIRouter(prefix="/api/hcps", tags=["HCPs"])

@router.post("/", response_model=HCPResponse)
def create_hcp(hcp: HCPCreate, db: Session = Depends(get_db)):
    """Create a new HCP record"""
    db_hcp = HCP(**hcp.dict())
    db.add(db_hcp)
    db.commit()
    db.refresh(db_hcp)
    return db_hcp

@router.get("/{hcp_id}", response_model=HCPResponse)
def get_hcp(hcp_id: int, db: Session = Depends(get_db)):
    """Get HCP by ID"""
    db_hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not db_hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    return db_hcp

@router.get("/", response_model=list[HCPResponse])
def list_hcps(db: Session = Depends(get_db)):
    """List all HCPs"""
    return db.query(HCP).all()

@router.put("/{hcp_id}", response_model=HCPResponse)
def update_hcp(hcp_id: int, hcp: HCPUpdate, db: Session = Depends(get_db)):
    """Update HCP"""
    db_hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not db_hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    
    update_data = hcp.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_hcp, field, value)
    
    db_hcp.updated_at = datetime.utcnow()
    db.add(db_hcp)
    db.commit()
    db.refresh(db_hcp)
    return db_hcp

@router.delete("/{hcp_id}")
def delete_hcp(hcp_id: int, db: Session = Depends(get_db)):
    """Delete HCP"""
    db_hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not db_hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    
    db.delete(db_hcp)
    db.commit()
    return {"detail": "HCP deleted successfully"}
