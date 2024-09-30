from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import selectinload, joinedload

from src.app.notes.models import Note, Tag
from src.app.notes.schemas import NoteCreate, NoteResponse
from src.app.database import get_async_session
from src.app.auth.base_config import current_user
from src.app.auth.models import User


router = APIRouter(
    prefix="/note",
    tags=["note"]
)


@router.post("", response_model=NoteResponse)
async def create_note(
    note_data: NoteCreate, 
    db: AsyncSession = Depends(get_async_session), 
    user: User = Depends(current_user)
):
    new_note = Note(
        title=note_data.title,
        content=note_data.content,
        user_id=user.id
    )

    for tag_name in note_data.tags:
        result = await db.execute(select(Tag).filter_by(name=tag_name))
        tag = result.scalar_one_or_none()
        if tag is None:
            tag = Tag(name=tag_name)
            db.add(tag)
        new_note.tags.append(tag)

    db.add(new_note)
    await db.commit()

    new_note = await db.get(
        Note,
        new_note.id,
        options=(joinedload(Note.tags))
    )

    return new_note
    

@router.get("s", response_model=List[NoteResponse])
async def get_notes(
    tag: str = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    query = select(Note).filter_by(
        user_id=user.id
    ).options(selectinload(Note.tags)).offset(skip).limit(limit)

    if tag:
        query = query.join(Note.tags).filter(Tag.name == tag)

    result = await db.execute(query)
    notes = result.scalars().all()

    return notes

    
@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int, 
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    result = await db.execute(
        select(Note).filter_by(id=note_id).options(joinedload(Note.tags))
    )
    note = result.unique().scalar_one_or_none()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if note.user_id != user.id:
        raise HTTPException(status_code=403, detail="Note is not yours")

    return note


@router.delete("/{note_id}", response_model=NoteResponse)
async def delete_note(
    note_id: int, 
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    note = await get_note(note_id, db, user)
    await db.delete(note)
    await db.commit()

    return note
    

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int, 
    note_data: NoteCreate, 
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    note = await get_note(note_id, db, user)

    note.title = note_data.title
    note.content = note_data.content

    note.tags.clear()

    for tag_name in note_data.tags:
        result = await db.execute(select(Tag).filter_by(name=tag_name))
        tag = result.scalar_one_or_none()
        if tag is None:
            tag = Tag(name=tag_name)
            db.add(tag)
        note.tags.append(tag)

    await db.commit()
    await db.refresh(note)

    return note
