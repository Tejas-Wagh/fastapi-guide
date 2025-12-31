from fastapi import APIRouter, HTTPException, status as status_code
from models.blogModels import BlogUpsert, BlogResponse, GenerateBlog
from dbModels import Blog
from starlette import status
from database import db_dependency
from utils import user_dependency, generateBlog

router = APIRouter(
    tags=["blogs"]
)


@router.get("/blogs", status_code=status.HTTP_200_OK)
def get_blogs(db:db_dependency) -> list[BlogResponse]:
    blogs = db.query(Blog).all()
    return blogs


@router.get("/blog/{blog_id}", status_code=status.HTTP_200_OK)
def get_blog(blog_id:int, db:db_dependency) -> BlogResponse :
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(status_code=status_code.HTTP_404_NOT_FOUND, detail="Blog not found!")
    
    return blog

@router.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(blog:BlogUpsert, user:user_dependency,db:db_dependency):
   if not user:
       raise HTTPException(status_code=status_code.HTTP_401_UNAUTHORIZED, detail="Unauthorized user!")
   
   newBlog = Blog(
       title= blog.title,
       content= blog.content,
       user_id = user.get("id")
   )
   db.add(newBlog)
   db.commit()

   return {
       "message":"blog created!"
   }


@router.put("/blog/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_blog(blog_id:int, blog:BlogUpsert, db:db_dependency, user:user_dependency) :
    
    if not user:
        raise HTTPException(status_code=status_code.HTTP_401_UNAUTHORIZED, detail="Unauthorized user!")
    
    existing_blog = db.query(Blog).filter(Blog.id == blog_id).filter(Blog.user_id == user.get("id")).first()

    if not existing_blog:
        raise HTTPException(status_code=status_code.HTTP_404_NOT_FOUND, detail="Blog not found!")

    existing_blog.title = blog.title
    existing_blog.content = blog.content
    db.add(existing_blog)
    db.commit()

    return {
        "message":"blog updated!"
    }
    
   


@router.delete("/blog/{blog_id}", status_code=status.HTTP_200_OK)
def delete_blog(blog_id:int, db:db_dependency, user:user_dependency):
    blog = db.query(Blog).filter(Blog.id == blog_id).filter(Blog.user_id == user.get("id")).first()

    if not blog:
        raise HTTPException(status_code=status_code.HTTP_404_NOT_FOUND, detail="Blog not found")
    
    db.delete(blog)
    db.commit()

    return {
        "message":"blog deleted"
    }


@router.post("/blog/generate", status_code=status.HTTP_201_CREATED)
def generate_blog(blog_details:GenerateBlog,db:db_dependency, user:user_dependency):
    if not user:
        raise HTTPException(status_code=status_code.HTTP_401_UNAUTHORIZED, detail="Unauthorized user!")
    
    blog = generateBlog(blog_details)

    newBlog = Blog(
        title=blog_details.title,
        content=blog,
        user_id=user.get("id")
    )

    db.add(newBlog)
    db.commit()
    
    return {
        "message":"blog created!"
    }