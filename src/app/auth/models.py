from datetime import datetime
from typing import Annotated, List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import text, String, Table
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.app.database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    email: Mapped[str]
    username: Mapped[str]
    registered_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    hashed_password: Mapped[str] = mapped_column(String(length=1024))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)

    notes: Mapped[List["Note"]] = relationship(
        back_populates="user", 
        cascade="all"
    )