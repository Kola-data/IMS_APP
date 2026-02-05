from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.company_model import CompanyModel
from schemas.company_schema import (
    CompanyRegisterSchema, 
    CompanyListResponseSchema, 
    CompanyUpdateSchema,
)
import uuid


class CompanyServices:
    @staticmethod
    async def create_company(db: AsyncSession, company_data: CompanyRegisterSchema) -> CompanyModel:
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
    async def get_companies(db: AsyncSession) -> list[CompanyModel]:
        results = await db.execute(select(CompanyModel).where(CompanyModel.is_deleted == False)) 
       
        return results.scalars().all()
    
    @staticmethod
    async def get_company_by_id(db: AsyncSession, company_id: uuid.UUID) -> CompanyModel | None:
        single_company = await db.execute(select(CompanyModel).where(CompanyModel.id == company_id, CompanyModel.is_deleted == False))
    
        return single_company.scalars().first()
    
    @staticmethod
    async def update_company(db: AsyncSession, company_id: uuid.UUID, update_data: CompanyUpdateSchema) -> CompanyModel | None:
        company = await db.get(CompanyModel, company_id)
        if not company or company.is_deleted:
            return None

        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(company, key, value)

        db.add(company)
        await db.commit()
        await db.refresh(company)
        return company
    

    @staticmethod
    async def delete_company(db: AsyncSession, company_id: uuid.UUID) -> bool:
        company = await db.get(CompanyModel, company_id)
        
        if not company or company.is_deleted:
            return None
        
        company.is_deleted = True
        await db.commit()
        return True
    

    @staticmethod
    async def deactivate_company(db: AsyncSession, company_id: uuid.UUID) -> bool:
        company = await db.get(CompanyModel, company_id)
        if not company or company.is_deleted:
            return None
        company.is_active = False
        await db.commit()
        return True
    
    @staticmethod
    async def activate_company(db: AsyncSession, company_id: uuid.UUID) -> bool:
        company = await db.get(CompanyModel, company_id)
        if not company or company.is_deleted:
            return None
        company.is_active = True
        await db.commit()
        return True