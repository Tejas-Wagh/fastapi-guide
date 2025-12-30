from pydantic import BaseModel, Field
from datetime import datetime

class BlogResponse(BaseModel):
    id:int = Field(gt=0)
    title:str = Field(min_length=3, max_length=30)
    content:str = Field(min_length=10, max_length=500)
    published_on:datetime
    user_id:int = Field(gt=0)


class BlogUpsert(BaseModel):
    title:str = Field(min_length=3, max_length=30)
    content:str = Field(min_length=10, max_length=500)

