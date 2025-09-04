from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ServiceCategory(str, Enum):
    SERVICE_FB = "service_fb"
    HOUSEKEEPING = "housekeeping"
    MAINTENANCE = "maintenance"
    PORTER = "porter"
    CONCIERGE = "concierge"
    RECEPTION = "reception"

class CategoryResponse(BaseModel):
    category: ServiceCategory
    message: str = Field(..., description="AI-generated specific message for this service category")
    urgency: str = Field(..., description="low, medium, high - AI-determined urgency level")

class ClassificationRequest(BaseModel):
    guest_message: str = Field(..., description="The guest's message to classify")
    guest_id: Optional[str] = Field(None, description="Guest identifier")
    room_number: Optional[str] = Field(None, description="Guest's room number")

class ClassificationResponse(BaseModel):
    should_create_ticket: bool
    categories: List[CategoryResponse]
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str
    suggested_priority: str = Field(..., description="overall priority: low, medium, high, urgent")
    estimated_completion_time: Optional[str] = Field(None, description="AI estimated time to complete")

class HealthResponse(BaseModel):
    status: str
    model_status: str
    timestamp: str
