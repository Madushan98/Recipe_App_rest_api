from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import now 

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False,index=True)
    content = Column(String,index=True)
    recipe = Column(String,index=True)
    


