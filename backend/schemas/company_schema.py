from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
import uuid

class CompanyRegisterSchema(BaseModel):    
    name: str
    owner_name: str
    phone: str
    email: EmailStr
    address: str
    
    model_config = ConfigDict(from_attributes=True)

class CompanyUpdateSchema(BaseModel):
    name: Optional[str] = None
    owner_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class CompanyResponseSchema(BaseModel):
    id: uuid.UUID
    name: str
    owner_name: str
    phone: str
    email: EmailStr
    address: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class CompanyListResponseSchema(BaseModel):
    companies: list[CompanyResponseSchema]
    
    model_config = ConfigDict(from_attributes=True)
