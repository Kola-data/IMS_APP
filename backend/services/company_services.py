from db.db_conn import AsyncSessionLocal
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.company_model import CompanyModel
from schemas.company_schema import (
    CompanyRegisterSchema, 
    CompanyListResponseSchema, 
    CompanyUpdateSchema,
    CompanyResponseSchema
)
import uuid
from pydantic import BaseModel

class CompanyServices:
    @staticmethod
    async def create_company(db: AsyncSession, company_data: CompanyRegisterSchema) -> CompanyResponseSchema:
        new_company = CompanyModel(
            name = company_data.name,
            owner_name = company_data.owner_name,
            phone = company_data.phone,
            email = company_data.email,
            address = company_data.address
        )

        db.add(new_company)
        await db.commit()
        await db.refresh(new_company)
        return new_company
    
    @staticmethod
    async def get_companies(db: AsyncSession) -> CompanyListResponseSchema:
        results = await db.execute(select(CompanyModel))
        list_companies = results.scalars().all()
        if not list_companies:
            return {"message": "No companies found"}
        return {"companies": list_companies, "message": "Companies retrieved successfully"}
    
    @staticmethod
    async def get_company_by_id(db: AsyncSession, company_id: uuid.UUID) -> CompanyResponseSchema:
        single_company = await db.get(CompanyModel, company_id)
        if not single_company:
            return {"message": "Company not found"}
        return single_company
    
    @staticmethod
    async def update_company(db: AsyncSession, company_id: uuid.UUID, update_data: CompanyUpdateSchema) -> CompanyResponseSchema:
        company = await db.get(CompanyModel, company_id)
        if not company:
            return {"message": "Company not found"}

        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(company, key, value)

        db.add(company)
        await db.commit()
        await db.refresh(company)
        return company
    

    @staticmethod
    async def delete_company(db: AsyncSession, company_id: uuid.UUID) -> dict:
        company = await db.get(CompanyModel, company_id)
        if not company:
            return {"message": "Company not found"}
        await db.delete(company)
        await db.commit()
        return {"message": "Company deleted successfully"}