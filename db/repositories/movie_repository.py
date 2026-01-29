from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException
from db.models import Movie, GenreModel, DirectorModel, StarModel, CertificationModel
from db.schemas import MovieCreateSchema

class MovieRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Movie).all()

    def get_by_id(self, movie_id: UUID):
        movie = self.db.get(Movie, movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie

    def create(self, data: MovieCreateSchema):
        certification = self.db.get(CertificationModel, data.certification_id)
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
            movie.genres = self.db.query(GenreModel).filter(GenreModel.id.in_(data.genre_ids)).all()
        if data.director_ids:
            movie.directors = self.db.query(DirectorModel).filter(DirectorModel.id.in_(data.director_ids)).all()
        if data.star_ids:
            movie.stars = self.db.query(StarModel).filter(StarModel.id.in_(data.star_ids)).all()

        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie
