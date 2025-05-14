from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Annotated
from app.database.session import get_db

SessionDep = Annotated[Session, Depends(get_db)]