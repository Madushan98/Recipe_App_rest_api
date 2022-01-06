from typing import Optional
from fastapi import FastAPI,Depends,status,Response

from pydantic import BaseModel
import psycopg2
import time
import psycopg2.extras
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:

#         conn = psycopg2.connect(host= 'localhost', dbname='test', user="postgres", port = "5433", password="123" ) 
#         cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
#         print("Connection Successful")
#         break
#     except Exception as e:
#         print("Error : " + e.message)
#         print("Connection Failed")
#         time.sleep(2)       






class Post(BaseModel):
    content : Optional[str] = None
    recipe : Optional[str] = None
   


@app.get("/")
def read_root(db:Session =Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"posts": posts}


@app.post("/post")
def create_posts(post:Post,db: Session =Depends(get_db)):
    
    new_post = models.Post(**post.dict()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data" :new_post} 


@app.get("/posts/{id}")
def get_post(id:int,db:Session =Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with id:{id} not found")

    return {"post" : post}

@app.delete("/posts/{id}")
def get_post(id:int,db:Session =Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with id:{id} not found")

    post.delete(synchronize_session=False) 
    db.commit() 

    return Response(status_code=status.HTTP_204_NO_CONTENT)



# @app.get("/posts/{id}")
# async def read_root(id:int):
#     cursor.execute("""SELECT * FROM posts where "Id" = %s   """,(id,))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(409, detail="Error raised")
#     return {"posts": post}





