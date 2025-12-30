from pydantic import BaseModel, Field

class UserSignUp(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8)


class UserSignIn(BaseModel):
    username:str = Field(min_length=3, max_length=30)
    password:str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class AuthResponse(BaseModel):
    access_token:str
    token_type:str



