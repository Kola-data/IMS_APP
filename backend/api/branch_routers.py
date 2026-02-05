from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from services.branch_services import BranchServices

from db.db_conn import AsyncSessionLocal

from schemas.branch_schema import (
    BranchRegisterSchema,
    BranchResponseSchema,
    BranchListResponseSchema,
    BranchUpdateSchema,
    BranchResponse
)

router = APIRouter(
    prefix="/branches",
    tags=["Branches"]
)
import uuid


@router.post("/", response_model=BranchResponse)
async def create_branch(branch_data: BranchRegisterSchema):
    async with AsyncSessionLocal() as db:
        result = await BranchServices.create_branch(db, branch_data)
        if not result:
            raise HTTPException(status_code=400, detail="Branch could not be created")
        return {
            "message": "Branch created successfully",
            "branch": result
        }
    
@router.get("/{branch_id}", response_model=BranchResponseSchema)
async def get_branch(branch_id: str, company_id: uuid.UUID):
    async with AsyncSessionLocal() as db:
        result = await BranchServices.get_branch_by_id(db, branch_id, company_id)
        if not result:
            raise HTTPException(status_code=404, detail="Branch not found")
        return result
    
@router.get("/", response_model=BranchListResponseSchema)
async def get_branches(company_id: uuid.UUID):
    async with AsyncSessionLocal() as db:
        result = await BranchServices.get_branches(db, company_id)
        
        return {"branches": result}
    
@router.put("/{branch_id}", response_model=BranchResponse)
async def update_branch(branch_id: str, company_id: uuid.UUID, update_data: BranchUpdateSchema):
    async with AsyncSessionLocal() as db:
        result = await BranchServices.update_branch(db, branch_id, company_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail="Branch not found")
        return {
            "message": "Branch updated successfully",
            "branch": result
            }
            
   
@router.delete("/{branch_id}")
async def delete_branch(branch_id: str, company_id: uuid.UUID):
    async with AsyncSessionLocal() as db:
        result = await BranchServices.delete_branch(db, branch_id, company_id)
        if not result:
            raise HTTPException(status_code=404, detail="Branch not found")
        return {"message": "Branch deleted successfully"}
    
@router.patch("/{branch_id}/deactivate")
async def deactivate_branch(branch_id: str, company_id: uuid.UUID):
    async with AsyncSessionLocal() as db:
        result = await BranchServices.deactivate_branch(db, branch_id, company_id)
        if not result:
            raise HTTPException(status_code=404, detail="Branch not found")
        return {
            "message": "Branch deactivated successfully",
            "status": result
        }
    
@router.patch("/{branch_id}/activate")
async def activate_branch(branch_id: str, company_id: uuid.UUID):
    async with AsyncSessionLocal() as db:
        result = await BranchServices.activate_branch(db, branch_id, company_id)
        if not result:
            raise HTTPException(status_code=404, detail="Branch not found")
        return {
            "message": "Branch activated successfully",
            "status": result
        }