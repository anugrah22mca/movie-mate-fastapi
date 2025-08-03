from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/media", response_model=list[schemas.Media])
def read_media(db: Session = Depends(get_db)):
    return crud.get_media(db)

@router.post("/media", response_model=schemas.Media)
def add_media(media: schemas.MediaCreate, db: Session = Depends(get_db)):
    return crud.create_media(db, media)
