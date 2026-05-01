from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db import get_db
from app.models.card import Card
from app.models.page import Page
from app.schemas import CardCreate, CardUpdate, CardResponse
from app.auth import get_current_user

router = APIRouter(prefix="/cards", tags=["cards"])


@router.get("/", response_model=list[CardResponse])
def list_cards(
    page_id: int = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    uid = current_user["sub"]
    q = db.query(Card).filter(
        or_(Card.created_by == uid, Card.created_by.is_(None))
    )
    if page_id is not None:
        q = q.filter(Card.page_id == page_id)
    return q.all()


@router.get("/{card_id}", response_model=CardResponse)
def get_card(card_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    uid = current_user["sub"]
    card = db.query(Card).filter(
        Card.id == card_id,
        or_(Card.created_by == uid, Card.created_by.is_(None))
    ).first()
    if card is None:
        raise HTTPException(404, detail="Card not found")
    return card


@router.post("/", response_model=CardResponse, status_code=201)
def create_card(body: CardCreate, page_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db.query(Page).filter(Page.id == page_id).first():
        raise HTTPException(404, detail="No such page")

    card = Card(page_id=page_id, created_by=current_user["sub"], **body.model_dump())
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


@router.put("/{card_id}", response_model=CardResponse)
def update_card(
    card_id: int,
    body: CardUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    card = db.query(Card).filter(Card.id == card_id).first()
    if card is None:
        raise HTTPException(404, detail="Card not found")

    changes = body.model_dump(exclude_unset=True)
    for k, v in changes.items():
        setattr(card, k, v)
    db.commit()
    db.refresh(card)
    return card


@router.delete("/{card_id}", status_code=204)
def delete_card(card_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if card is None:
        raise HTTPException(404, detail="Card not found")
    db.delete(card)
    db.commit()
