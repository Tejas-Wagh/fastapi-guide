from fastapi import FastAPI
from dotenv import load_dotenv
from routers.auth import router as auth_router
from routers.blog import router as blog_router
from database import engine
import dbModels

load_dotenv()

dbModels.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(blog_router)

@app.get("/")
def read_root():
    return {"message":"hello world"}

