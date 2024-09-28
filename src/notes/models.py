from __future__ import annotations
from datetime import datetime
from typing import Annotated, List

from sqlalchemy import Table, Column, Integer, ForeignKey, text
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.database import Base
from src.notes.utils import naive_utcnow


intpk = Annotated[int, mapped_column(primary_key=True)]


note_tag_table = Table(
    'note_tag', 
    Base.metadata,
    Column('note_id', Integer, ForeignKey('note.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True)
)


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[intpk] 
    name: Mapped[str]

    notes: Mapped[List[Note]] = relationship(
        secondary=note_tag_table, 
        back_populates="tags"
    )


class Note(Base):
    __tablename__ = "note"

    id: Mapped[intpk] 
    title: Mapped[str]
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=naive_utcnow
    )

    tags: Mapped[List[Tag]] = relationship(
        secondary=note_tag_table, 
        back_populates="notes",
        cascade="all"
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="notes")

    # owner_id = Column(Integer, ForeignKey("users.id"))
    # owner = relationship("User", back_populates="items")

