from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from db.database import SessionLocal, Base, engine

app = FastAPI()

