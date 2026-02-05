from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.branch_model import BranchModel
from schemas.branch_schema import (
    BranchRegisterSchema, 
    BranchUpdateSchema,
    
    )

import uuid

class BranchServices:
    @staticmethod
    async def create_branch(db: AsyncSession, branch_data: BranchRegisterSchema) -> BranchModel:
        
        new_branch = BranchModel (
            name = branch_data.name,
            location = branch_data.location,
            branch_manager = branch_data.branch_manager,
            branch_contacts = branch_data.branch_contacts,
            company_id = branch_data.company_id
        )

        db.add(new_branch)
        await db.commit()
        await db.refresh(new_branch)
        return new_branch
    
    @staticmethod
    async def get_branches(db: AsyncSession, company_id: uuid.UUID) -> list[BranchModel]:
        
        all_branches = await db.execute(select(BranchModel).where(BranchModel.is_deleted == False, BranchModel.is_active == True, BranchModel.company_id == company_id))
        return all_branches.scalars().all()
      
    
    @staticmethod
    async def get_branch_by_id(db: AsyncSession, branch_id: uuid.UUID, company_id: uuid.UUID) -> BranchModel | None:
        result = await db.execute(select(BranchModel).where(BranchModel.id == branch_id, BranchModel.is_deleted == False, BranchModel.is_active == True, BranchModel.company_id == company_id))
        single_branch = result.scalars().first()
        
        if not single_branch or single_branch.is_deleted:
            return None
        return single_branch
    
    @staticmethod
    async def update_branch(db: AsyncSession, branch_id: uuid.UUID, company_id: uuid.UUID, update_data: BranchUpdateSchema) -> BranchModel | None:
        result = await db.execute(select(BranchModel).where(BranchModel.id == branch_id, BranchModel.is_deleted == False, BranchModel.is_active == True, BranchModel.company_id == company_id))
        branch = result.scalars().first()
        
        if not branch or branch.is_deleted:
            return None
        
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(branch, key, value)

        db.add(branch)
        await db.commit()
        await db.refresh(branch)
        return branch
    
    @staticmethod
    async def delete_branch(db: AsyncSession, branch_id: uuid.UUID, company_id: uuid.UUID) -> bool:
        branch = await db.execute(select(BranchModel).where(BranchModel.id == branch_id, BranchModel.is_deleted == False, BranchModel.company_id == company_id))
        branch = branch.scalars().first()
        
        
        branch.is_deleted = True
        await db.commit()
        return True
    
    @staticmethod
    async def deactivate_branch(db: AsyncSession, branch_id: uuid.UUID, company_id: uuid.UUID) -> bool:
        branch = await db.execute(select(BranchModel).where(BranchModel.id == branch_id, BranchModel.is_deleted == False, BranchModel.company_id == company_id))
        branch = branch.scalars().first()
        
        if not branch or branch.is_deleted:
            return False
        
        branch.is_active = False
        await db.commit()
        return True
    
    @staticmethod
    async def activate_branch(db: AsyncSession, branch_id: uuid.UUID, company_id: uuid.UUID) -> bool:
        branch = await db.execute(select(BranchModel).where(BranchModel.id == branch_id, BranchModel.is_deleted == False, BranchModel.company_id == company_id))
        branch = branch.scalars().first()
        
        if not branch or branch.is_deleted:
            return False
        
        branch.is_active = True
        await db.commit()
        return True