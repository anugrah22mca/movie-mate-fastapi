# backend/app/routes/recommendations.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from collections import defaultdict
from sqlalchemy.sql import func
from app import models, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/recommendations", response_model=list[schemas.Media])
def get_recommendations(db: Session = Depends(get_db)):
    # Step 1: Join Media + Reviews to get rated media
    reviewed_media = (
        db.query(models.Media.genre, models.Review.rating)
        .join(models.Review, models.Media.id == models.Review.media_id)
        .filter(models.Review.rating.isnot(None))
        .all()
    )

    if not reviewed_media:
        return []

    # Step 2: Aggregate average rating per genre
    genre_ratings = defaultdict(list)
    for genre, rating in reviewed_media:
        genre_ratings[genre].append(rating)

    genre_avg = {
        genre: sum(ratings) / len(ratings)
        for genre, ratings in genre_ratings.items()
    }

    # Step 3: Pick top genre
    top_genre = max(genre_avg, key=genre_avg.get)

    # Step 4: Recommend media of that genre with no reviews yet
    subquery = db.query(models.Review.media_id).distinct()
    recommended = (
        db.query(models.Media)
        .filter(
            models.Media.genre == top_genre,
            ~models.Media.id.in_(subquery)
        )
        .limit(10)
        .all()
    )

    return recommended
