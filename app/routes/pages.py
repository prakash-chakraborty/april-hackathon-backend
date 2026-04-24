from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.page import Page
from app.schemas import PageCreate, PageUpdate, PageResponse
from app.auth import get_current_user

router = APIRouter(prefix="/pages", tags=["pages"])


@router.get("/", response_model=list[PageResponse])
def list_pages(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # TODO: add pagination at some point
    return db.query(Page).all()


@router.get("/{page_id}", response_model=PageResponse)
def get_page(page_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.id == page_id).first()
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found")
    return page


@router.post("/", response_model=PageResponse, status_code=201)
def create_page(data: PageCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    page = Page(name=data.name)
    db.add(page)
    db.commit()
    db.refresh(page)
    return page


@router.put("/{page_id}", response_model=PageResponse)
def update_page(
    page_id: int,
    data: PageUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    page = db.query(Page).filter(Page.id == page_id).first()
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found")

    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(page, key, val)

    db.commit()
    db.refresh(page)
    return page


@router.delete("/{page_id}", status_code=204)
def delete_page(page_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.id == page_id).first()
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found")
    db.delete(page)
    db.commit()
