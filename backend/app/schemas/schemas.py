from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

class InteractionType(str, Enum):
    CALL = "call"
    MEETING = "meeting"
    EMAIL = "email"
    CONFERENCE = "conference"
    WEBINAR = "webinar"

class HCPBase(BaseModel):
    name: str
    specialty: Optional[str] = None
    organization: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

class HCPCreate(HCPBase):
    pass

class HCPUpdate(BaseModel):
    name: Optional[str] = None
    specialty: Optional[str] = None
    organization: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

class HCPResponse(HCPBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FollowUpBase(BaseModel):
    action_item: str
    due_date: Optional[datetime] = None
    completed: bool = False

class FollowUpCreate(FollowUpBase):
    interaction_id: int

class FollowUpResponse(FollowUpBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class InteractionBase(BaseModel):
    interaction_type: InteractionType
    title: str
    description: Optional[str] = None

class InteractionCreate(InteractionBase):
    hcp_id: int

class InteractionUpdate(BaseModel):
    interaction_type: Optional[InteractionType] = None
    title: Optional[str] = None
    description: Optional[str] = None

class InteractionResponse(InteractionBase):
    id: int
    hcp_id: int
    summary: Optional[str] = None
    date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatMessage(BaseModel):
    message: str
    hcp_id: Optional[int] = None
    mode: Optional[str] = None
    existing_form: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    interaction_id: Optional[int] = None
    action_items: Optional[List[str]] = None
    form_data: Optional[Dict[str, Any]] = None
