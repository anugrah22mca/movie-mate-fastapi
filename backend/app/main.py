from fastapi import FastAPI
from . import models
from .database import engine
from .routes import media, episodes, reviews, recommendations, generateReview
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(media.router)
app.include_router(episodes.router)
app.include_router(reviews.router)
app.include_router(recommendations.router)
app.include_router(generateReview.router)