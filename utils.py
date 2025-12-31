import os
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from openai import OpenAI
from prompt import SYSTEM_PROMPT
from models.blogModels import GenerateBlog

load_dotenv()

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/sign-in")
client = OpenAI()

def create_access_token(user_id:int, username:str) -> str:
    data = {
        "sub":username,
        "id":user_id
    }

    expires = datetime.utcnow() + timedelta(minutes=30)
    token = jwt.encode(data, os.getenv("SECRET_KEY"))

    return token


def verify_access_token(token:Annotated[str, Depends(oauth2_bearer)]):
    try: 
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        username = payload.get("sub")
        user_id = payload.get("id")

        if not username or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        
        return {
            "email":username,
            "id":user_id
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    
user_dependency = Annotated[dict, Depends(verify_access_token)]



def generateBlog(blog_details : GenerateBlog):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },
            {
                "role":"user",
                "content":f"""
                    Title: {blog_details.title}
                    Desired Length: {blog_details.desired_length}
                    Target Audience: {blog_details.target_audience}
                    Tone: {blog_details.tone}
                """
            }
        ]
    )

    result = response.choices[0].message.content

    return result
    