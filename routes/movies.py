from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Movie, GenreModel, DirectorModel, StarModel, CertificationModel
from db.schemas import (
    MovieCreateSchema,
    MovieBaseSchema,
)