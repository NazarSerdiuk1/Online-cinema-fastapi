from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from db.database import get_db
from db.repositories.movie_repository import MovieRepository
from db.schemas import MovieCreateSchema, MovieBaseSchema

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.post("/", response_model=MovieBaseSchema)
def create_movie(
    data: MovieCreateSchema,
    db: Session = Depends(get_db),
):
    repo = MovieRepository(db)
    return repo.create(data)

@router.get("/", response_model=list[MovieBaseSchema])
def list_movies(db: Session = Depends(get_db)):
    repo = MovieRepository(db)
    return repo.get_all()

@router.get("/{movie_id}", response_model=MovieBaseSchema)
def get_movie(movie_id: UUID, db: Session = Depends(get_db)):
    repo = MovieRepository(db)
    return repo.get_by_id(movie_id)
