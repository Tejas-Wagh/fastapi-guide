from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BlogResponse(BaseModel):
    id:int = Field(gt=0)
    title:str = Field(min_length=3, max_length=30)
    content:str 
    published_on:datetime
    user_id:int = Field(gt=0)


class BlogUpsert(BaseModel):
    title:str = Field(min_length=3, max_length=30)
    content:str



class GenerateBlog(BaseModel):
    title:str = Field(min_length=3, max_length=30)
    desired_length:int = Field(gt=0)
    target_audience:Optional[str] = Field(default=None, min_length=3, max_length=30)
    tone: Optional[str] = Field(default=None, min_length=3, max_length=30)
