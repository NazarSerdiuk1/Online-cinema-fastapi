from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from db.database import get_db
from db.models import Movie, GenreModel, DirectorModel, StarModel, CertificationModel
from db.schemas import (
    MovieCreateSchema,
    MovieBaseSchema,
)

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.post(
    "/",
    response_model=MovieBaseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    data: MovieCreateSchema,
    db: Session = Depends(get_db),
):
    certification = db.get(CertificationModel, data.certification_id)
    if not certification:
        raise HTTPException(status_code=404, detail="Certification not found")

    movie = Movie(
        name=data.name,
        year=data.year,
        time=data.time,
        imdb=data.imdb,
        votes=data.votes,
        description=data.description,
        price=data.price,
        certification_id=data.certification_id,
    )

    if data.genre_ids:
        movie.genres = db.query(GenreModel).filter(
            GenreModel.id.in_(data.genre_ids)
        ).all()

    if data.director_ids:
        movie.directors = db.query(DirectorModel).filter(
            DirectorModel.id.in_(data.director_ids)
        ).all()

    if data.star_ids:
        movie.stars = db.query(StarModel).filter(
            StarModel.id.in_(data.star_ids)
        ).all()

    db.add(movie)
    db.commit()
    db.refresh(movie)

    return movie

@router.get("/", response_model=list[MovieBaseSchema])
def list_movies(
    db: Session = Depends(get_db),
):
    return db.query(Movie).all()

@router.get("/{movie_id}", response_model=MovieBaseSchema)
def get_movie(
    movie_id: UUID,
    db: Session = Depends(get_db),
):
    movie = db.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie