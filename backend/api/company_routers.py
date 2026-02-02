from fastapi import APIRouter
from services.company_services import CompanyServices
from schemas.company_schema import (
    CompanyRegisterSchema,
    CompanyResponseSchema,
    CompanyListResponseSchema
)
from db.db_conn import AsyncSessionLocal

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

@router.post("/", response_model=CompanyResponseSchema)
async def create_company(company_data: CompanyRegisterSchema):
    async with AsyncSessionLocal() as db:
        result = await CompanyServices.create_company(db, company_data)
        if not result:
            return {"message": "Company creation failed"}
        return result
    
@router.get("/{company_id}", response_model=CompanyResponseSchema)
async def get_company(company_id: str):
    async with AsyncSessionLocal() as db:
        result = await CompanyServices.get_company_by_id(db, company_id)
        return result
    
@router.get("/", response_model=CompanyListResponseSchema)
async def get_companies():
    async with AsyncSessionLocal() as db:
        result = await CompanyServices.get_companies(db)
        return result
    
@router.put("/{company_id}", response_model=CompanyResponseSchema)
async def update_company(company_id: str, update_data: CompanyRegisterSchema):
    async with AsyncSessionLocal() as db:
        result = await CompanyServices.update_company(db, company_id, update_data)
        return result
    
@router.delete("/{company_id}")
async def delete_company(company_id: str):
    async with AsyncSessionLocal() as db:
        result = await CompanyServices.delete_company(db, company_id)
        return result