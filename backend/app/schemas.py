from pydantic import BaseModel, Field, model_validator
from typing import Optional
from sqlalchemy import Column, Integer
from .database import Base
class MediaBase(BaseModel):
    title: str
    director: str
    type: str
    totalEpisodes: Optional[int] = Field(None, ge=1)
    genre: str
    platform: str
    status: str
    
    class Config:
        from_attributes = True
  
class MediaCreate(MediaBase):
    pass

class Media(MediaBase):
    id: int

    class Config:
        from_attributes = True
class EpisodeProgressBase(BaseModel):
    media_id: int
    season: int
    episode: int
    status: str

class EpisodeProgressCreate(EpisodeProgressBase):
    pass

class EpisodeProgress(EpisodeProgressBase):
    id: int
    class Config:
        orm_mode = True

# --- Review ---
class ReviewBase(BaseModel):
    media_id: int
    rating: int
    review_text: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    class Config:
        orm_mode = True
        
class EpisodeUpdate(BaseModel):
    season: int
    episode: int
    status: str