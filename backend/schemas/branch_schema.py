from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class BranchRegisterSchema(BaseModel):
    name: str
    location: str
    branch_manager: str
    branch_contacts: Dict[str, Any] = Field(..., description="Contact details for the branch")
    company_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class BranchUpdateSchema(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    branch_manager: Optional[str] = None
    branch_contacts: Optional[Dict[str, Any]] = Field(None, description="Contact details for the branch")

    model_config = ConfigDict(from_attributes=True)

class BranchResponseSchema(BaseModel):
    id: uuid.UUID
    name: str
    location: str
    branch_manager: str
    branch_contacts: Dict[str, Any]
    company_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class BranchResponse(BaseModel):
    message: str
    branch: BranchResponseSchema

class BranchListResponseSchema(BaseModel):
    branches: list[BranchResponseSchema]

    model_config = ConfigDict(from_attributes=True)
