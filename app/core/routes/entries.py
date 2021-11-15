import logging
from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.core.models.entry import Entry
from app.core.schemas.entry import EntryInCreate, EntryInResponse
from app.database import get_db

logger = logging.getLogger("app")

router = APIRouter(tags=["entries"], prefix="/entries")


@router.get(
    "/",
    summary="Get entries list by page",
    response_model=Page[EntryInResponse],
)
async def get_entries(
    db: Session = Depends(get_db),
    date_from: Optional[datetime] = Query(
        None,
        alias="dateFrom",
        description="Filter by date (minimum)",
    ),
    date_to: Optional[datetime] = Query(
        None,
        alias="dateTo",
        description="Filter by date (maximum)",
    ),
) -> Any:
    query = db.query(Entry)
    if date_from is not None:
        query = query.filter(Entry.created >= date_from)
    if date_to is not None:
        query = query.filter(Entry.created <= date_to)
    return paginate(query)


@router.get(
    "/{entry_id}",
    summary="Get entry by ID",
    response_model=EntryInResponse,
)
async def get_entry(
    db: Session = Depends(get_db),
    entry_id: UUID4 = Query(None, alias="id", description="ID of the entry to get"),
) -> EntryInResponse:
    try:
        entry = db.query(Entry).filter(Entry.id == entry_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return EntryInResponse.from_orm(entry)


@router.post(
    "/",
    summary="Post new entry",
    response_model=EntryInResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_entry(
    db: Session = Depends(get_db),
    entry_data: EntryInCreate = Body(...),
) -> EntryInResponse:
    try:
        entry = Entry(**entry_data.dict())
        db.add(entry)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return EntryInResponse.from_orm(entry)
