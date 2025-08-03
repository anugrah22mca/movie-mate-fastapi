from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/reviews", response_model=schemas.Review)
def add_review(data: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.add_review(db, data)

@router.get("/reviews/{media_id}", response_model=list[schemas.Review])
def get_reviews(media_id: int, db: Session = Depends(get_db)):
    return crud.get_reviews_for_media(db, media_id)
