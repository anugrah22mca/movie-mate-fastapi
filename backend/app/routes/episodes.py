from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal
from .. import models
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/episodes", response_model=schemas.EpisodeProgress)
def add_episode(data: schemas.EpisodeProgressCreate, db: Session = Depends(get_db)):
    return crud.add_episode(db, data)

@router.get("/episodes/{media_id}", response_model=list[schemas.EpisodeProgress])
def get_episodes(media_id: int, db: Session = Depends(get_db)):
    return crud.get_episodes_for_media(db, media_id)

@router.put("/episodes/{episode_id}", response_model=schemas.EpisodeUpdate)
def update_episode(episode_id: int, data: schemas.EpisodeUpdate, db: Session = Depends(get_db)):
    episode = db.query(models.EpisodeProgress).filter(models.EpisodeProgress.id == episode_id).first()
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    episode.season = data.season
    episode.episode = data.episode
    episode.status = data.status
    db.commit()
    db.refresh(episode)
    return episode