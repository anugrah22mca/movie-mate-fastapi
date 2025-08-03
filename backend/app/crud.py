from sqlalchemy.orm import Session
from . import models, schemas

def get_media(db: Session):
    return db.query(models.Media).all()

def create_media(db: Session, media: schemas.MediaCreate):
    db_media = models.Media(**media.dict())
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media
def add_episode(db: Session, data: schemas.EpisodeProgressCreate):
    db_ep = models.EpisodeProgress(**data.dict())
    db.add(db_ep)
    db.commit()
    db.refresh(db_ep)
    return db_ep

def get_episodes_for_media(db: Session, media_id: int):
    return db.query(models.EpisodeProgress).filter(models.EpisodeProgress.media_id == media_id).all()


def add_review(db: Session, data: schemas.ReviewCreate):
    db_review = models.Review(**data.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews_for_media(db: Session, media_id: int):
    return db.query(models.Review).filter(models.Review.media_id == media_id).all()