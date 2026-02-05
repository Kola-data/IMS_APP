
from sqlite3 import IntegrityError
from fastapi import APIRouter, HTTPException, status
from services.company_services import CompanyServices
from schemas.company_schema import (
    CompanyCreateResponse,
    CompanyRegisterSchema,
    CompanyResponseSchema,
    CompanyListResponseSchema
)
from db.db_conn import AsyncSessionLocal

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

@router.post("/", response_model=CompanyCreateResponse) # Ensure this is updated
async def create_company(company_data: CompanyRegisterSchema):
    async with AsyncSessionLocal() as db:
        try:
            result = await CompanyServices.create_company(db, company_data)
            return {
                "message": "Company created successfully",
                "company": result
            }
        except IntegrityError as e:
            await db.rollback()
            # This catches the 'companies_email_key' violation
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A company with this email already exists."
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred."
            )
    
@router.get("/{company_id}", response_model=CompanyResponseSchema)
async def get_company(company_id: str):
    async with AsyncSessionLocal() as db:
        result = await CompanyServices.get_company_by_id(db, company_id)
        if not result:
            raise HTTPException(status_code=404, detail="Company not found")
        return result
    
@router.get("/", response_model=list[CompanyResponseSchema])
async def get_companies():
    async with AsyncSessionLocal() as db:
        result = await CompanyServices.get_companies(db)
        
        return result
    
@router.put("/{company_id}", response_model=CompanyCreateResponse)
async def update_company(company_id: str, update_data: CompanyRegisterSchema):
    async with AsyncSessionLocal() as db:
        result = await CompanyServices.update_company(db, company_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail="Company not found")
        return {
                "message": "Company updated successfully",
                "company": result
        }
    
@router.delete("/{company_id}")
async def delete_company(company_id: str):
    async with AsyncSessionLocal() as db:
        result = await CompanyServices.delete_company(db, company_id)
        if not result:
            raise HTTPException(status_code=404, detail="Company not found")
        return {"message": "Company deleted successfully"}
    
@router.patch("/{company_id}/deactivate")
async def deactivate_company(company_id: str):
    async with AsyncSessionLocal() as db:
        company = await CompanyServices.get_company_by_id(db, company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        company.is_active = False
        db.add(company)
        await db.commit()
        await db.refresh(company)
        
        return {
            "message": "Company deactivated successfully",
            "company": company
        }
@router.patch("/{company_id}/activate")
async def activate_company(company_id: str):   
    async with AsyncSessionLocal() as db:
        company = await CompanyServices.get_company_by_id(db, company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        company.is_active = True
        db.add(company)
        await db.commit()
        await db.refresh(company)
        
        return {
            "message": "Company activated successfully",
            "company": company
        }