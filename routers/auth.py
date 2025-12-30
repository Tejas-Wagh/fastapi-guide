from fastapi import APIRouter, HTTPException, status as status_code, Depends
from models.authModels import UserSignIn, UserSignUp, UserResponse, AuthResponse
from starlette import status
from dbModels import User
from database import db_dependency
from passlib.context import CryptContext
from utils import create_access_token, user_dependency
from fastapi.security import OAuth2PasswordRequestForm

bcrypt_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/sign-up", status_code=status.HTTP_200_OK)
def sign_up(user:UserSignUp, db : db_dependency) -> AuthResponse | str:
  
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=status_code.HTTP_409_CONFLICT, detail="User already available!")
    
    hashed_pwd = bcrypt_ctx.hash(user.password)        
    new_user = User(
        username = user.username,
        email = user.email,
        password = hashed_pwd
    )

    db.add(new_user)
    db.commit()

    token = create_access_token(new_user.id, new_user.username)

    return {
        "access_token":token,
        "token_type": "bearer"
    }
    
    
   

@router.post("/sign-in", status_code=status.HTTP_200_OK)
def sign_in(db:db_dependency, user:OAuth2PasswordRequestForm = Depends()) -> AuthResponse:
    existing_user = db.query(User).filter(User.email == user.username).first()
    
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    
    if not bcrypt_ctx.verify(user.password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials!")
    
    token = create_access_token(existing_user.id, existing_user.username)

    return {
        "access_token":token,
        "token_type": "bearer"  
    }

@router.get("/user", status_code=status.HTTP_200_OK)
def get_user(db:db_dependency, user:user_dependency) -> UserResponse:
    existing_user = db.query(User).filter(User.id == user.get("id")).first()

    if not existing_user:
        raise HTTPException(status_code=status_code.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "id":existing_user.id,
        "username":existing_user.username,
        "email":existing_user.email
    }


@router.delete("/user", status_code=status.HTTP_200_OK)
def delete_user(db:db_dependency, user:user_dependency) :
    existing_user = db.query(User).filter(User.id == user.get("id")).first()

    if not existing_user:
        raise HTTPException(status_code=status_code.HTTP_404_NOT_FOUND, detail="User not found!")
    
    db.delete(existing_user)
    db.commit()
    return {
        "message":"User deleted",
    }
