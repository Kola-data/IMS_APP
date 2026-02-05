from datetime import datetime
import uuid
from typing import Dict, Any
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from db.db_conn import Base

class BranchModel(Base):
    __tablename__ = "branches"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(500), nullable=False)
    branch_manager: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Store contact object here
    branch_contacts: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    
    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
