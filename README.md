# FastAPI Blog API - Complete Beginner's Guide

A step-by-step guide to building a modern blog API with FastAPI. Perfect for developers new to FastAPI who want to learn authentication, database operations, and API development.

## What You'll Learn

- 🚀 **FastAPI Basics** - How to create fast, modern APIs with Python
- 🔐 **JWT Authentication** - Secure user login/registration system
- 📊 **SQLAlchemy ORM** - Work with databases using Python objects (no SQL required!)
- 🐘 **PostgreSQL Integration** - Connect and manage a real database
- 🔒 **Password Security** - Hash passwords safely with Bcrypt
- 📝 **CRUD Operations** - Create, Read, Update, Delete data
- 🛣️ **API Organization** - Structure your code like a pro
- 📚 **Auto Documentation** - Get beautiful API docs for free!

## What is FastAPI?

FastAPI is a modern Python web framework that makes building APIs incredibly easy and fast. It automatically:
- Validates your data
- Generates interactive documentation
- Provides excellent performance
- Offers great developer experience with auto-completion

## Tech Stack Explained

- **FastAPI**: The web framework (like Flask/Django but faster and easier)
- **PostgreSQL**: Our database (stores users and blog posts)
- **SQLAlchemy**: Lets us work with the database using Python objects
- **JWT**: Secure tokens for user authentication (like digital ID cards)
- **Bcrypt**: Encrypts passwords so they're safe
- **Pydantic**: Validates data automatically (built into FastAPI)

## Project Structure

```
fastapi-blog/
├── models/
│   ├── authModels.py      # Pydantic models for authentication
│   └── blogModels.py      # Pydantic models for blog operations
├── routers/
│   ├── auth.py           # Authentication routes
│   └── blog.py           # Blog CRUD routes
├── database.py           # Database configuration and connection
├── dbModels.py          # SQLAlchemy database models
├── main.py              # FastAPI application entry point
├── utils.py             # Utility functions (JWT, dependencies)
├── .env.example         # Environment variables template
└── pyproject.toml       # Project dependencies
```

## Complete Setup Guide for Beginners

### What You Need First

- **Python 3.13+** - [Download here](https://python.org/downloads/)
- **PostgreSQL** - [Download here](https://postgresql.org/download/) or use [PostgreSQL.app](https://postgresapp.com/) on Mac
- **Code Editor** - VS Code, PyCharm, or any editor you like
- **Terminal/Command Prompt** - Built into your OS

### Step-by-Step Installation

#### 1. Get the Code
```bash
# Download this project
git clone <repository-url>
cd fastapi-blog
```

#### 2. Install Python Packages
```bash
# Option 1: Using UV (faster, recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh  # Install UV first
uv sync  # Install all dependencies

# Option 2: Using regular pip
pip install fastapi sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-dotenv
```

#### 3. Set Up Your Database

**Create a PostgreSQL database:**
```bash
# Connect to PostgreSQL (you might need to adjust the command)
psql -U postgres

# Inside PostgreSQL, create your database
CREATE DATABASE fastapi_blog;
\q  # Exit PostgreSQL
```

#### 4. Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env
```

**Edit the `.env` file with your details:**
```env
# Replace with your actual database info
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/fastapi_blog

# Generate a secret key (or use this example for learning)
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
```

#### 5. Start Your API
```bash
# Using UV
uv run fastapi dev main.py

# Or using uvicorn directly
uvicorn main:app --reload
```

#### 6. Test It Works!
Open your browser and go to:
- **Your API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs ← This is amazing!
- **Alternative Docs**: http://localhost:8000/redoc

🎉 **Success!** You should see "hello world" at the main URL and beautiful API documentation at `/docs`

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/sign-up` | Register new user | No |
| POST | `/auth/sign-in` | Login user | No |
| GET | `/auth/user` | Get current user info | Yes |
| DELETE | `/auth/user` | Delete current user | Yes |

### Blog Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/blogs` | Get all blogs | No |
| GET | `/blog/{blog_id}` | Get specific blog | No |
| POST | `/blog` | Create new blog | Yes |
| PUT | `/blog/{blog_id}` | Update blog | Yes |
| DELETE | `/blog/{blog_id}` | Delete blog | Yes |

## Testing Your API (Beginner-Friendly)

### Method 1: Using the Interactive Docs (Easiest!)

1. Go to http://localhost:8000/docs
2. You'll see all your API endpoints with a "Try it out" button
3. Click any endpoint, fill in the data, and click "Execute"
4. See the response immediately!

### Method 2: Using curl Commands

#### 1. Create a New User
```bash
curl -X POST "http://localhost:8000/auth/sign-up" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```
**What happens**: Creates a new user and returns a JWT token

#### 2. Login (Get Your Token)
```bash
curl -X POST "http://localhost:8000/auth/sign-in" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=securepassword123"
```
**What happens**: Returns a JWT token you'll use for protected endpoints

#### 3. Create a Blog Post (Need Token)
```bash
# Replace YOUR_JWT_TOKEN with the actual token from step 2
curl -X POST "http://localhost:8000/blog" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is my first blog post using FastAPI!"
  }'
```
**What happens**: Creates a blog post linked to your user account

#### 4. Get All Blog Posts (No Token Needed)
```bash
curl -X GET "http://localhost:8000/blogs"
```
**What happens**: Returns all blog posts from all users

### Method 3: Using Python Requests
```python
import requests

# Register a user
response = requests.post("http://localhost:8000/auth/sign-up", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
})
token = response.json()["access_token"]

# Create a blog post
requests.post("http://localhost:8000/blog", 
    json={"title": "Test Post", "content": "Hello World!"},
    headers={"Authorization": f"Bearer {token}"}
)
```

## Database Models

### User Model
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Hashed password
```

### Blog Model
```python
class Blog(Base):
    __tablename__ = "blogs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    published_on = Column(DateTime(timezone=True), default=datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'))
```

## Authentication Flow

1. **Registration/Login**: User provides credentials
2. **JWT Token**: Server returns JWT token upon successful authentication
3. **Protected Routes**: Include token in Authorization header: `Bearer <token>`
4. **Token Validation**: Server validates token for protected endpoints

## Understanding the Code (For Beginners)

### How Authentication Works
```python
# When a user logs in, we create a JWT token
token = create_access_token(user.id, user.username)

# The token contains user info and expires after some time
# Users send this token with requests to prove who they are
# Think of it like a temporary ID card
```

**Why JWT?**
- No need to store sessions on the server
- Tokens contain all needed info
- Secure and scalable

### Database Models Explained
```python
# This creates a "users" table in your database
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)  # Unique ID for each user
    username = Column(String, index=True)   # Username (searchable)
    email = Column(String, unique=True)     # Email (must be unique)
    password = Column(String)               # Hashed password (never plain text!)
```

**SQLAlchemy Magic:**
- Write Python classes → Get database tables automatically
- No SQL required for basic operations
- Type safety and auto-completion

### CRUD Operations Made Simple
```python
# CREATE - Add new data
db.add(new_blog)
db.commit()

# READ - Get data
blogs = db.query(Blog).all()  # Get all blogs
blog = db.query(Blog).filter(Blog.id == 1).first()  # Get one blog

# UPDATE - Change existing data
blog.title = "New Title"
db.commit()

# DELETE - Remove data
db.delete(blog)
db.commit()
```

### API Router Organization
```python
# Instead of putting all routes in one file, we organize them:
# auth.py - handles login, signup, user management
# blog.py - handles blog creation, editing, deletion
# main.py - brings everything together

app.include_router(auth_router)  # Adds all auth routes
app.include_router(blog_router)  # Adds all blog routes
```

### Pydantic Models (Data Validation)
```python
# These models automatically validate incoming data
class BlogUpsert(BaseModel):
    title: str  # Must be a string
    content: str  # Must be a string
    
# If someone sends invalid data, FastAPI automatically returns an error
# No manual validation needed!
```

## Next Steps for Learning

### 1. Explore the Interactive Docs
- Go to http://localhost:8000/docs
- Try every endpoint
- Look at the request/response examples
- Notice how FastAPI generates this automatically!

### 2. Modify the Code
```python
# Try adding a new field to the Blog model
class Blog(Base):
    # ... existing fields ...
    tags = Column(String)  # Add this line
    
# Don't forget to update your Pydantic models too!
```

### 3. Add New Features
- Add blog categories
- Add user profiles
- Add comments on blogs
- Add like/dislike functionality

### 4. Learn More Advanced Topics
```bash
# Add proper testing
pip install pytest
# Create test_main.py and write tests

# Add database migrations (when you change models)
pip install alembic
alembic init alembic

# Add code formatting
pip install black isort
black .  # Formats your code
isort .  # Organizes imports
```

### 5. Deploy Your API
- Try deploying to Railway, Render, or Heroku
- Learn about environment variables in production
- Set up a production database

### 6. Common Beginner Mistakes to Avoid
- ❌ Don't store plain text passwords
- ❌ Don't commit your `.env` file to git
- ❌ Don't use the same secret key in production
- ❌ Don't forget to validate user input
- ✅ Always hash passwords
- ✅ Use environment variables for secrets
- ✅ Let FastAPI handle validation for you

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/db` |
| `SECRET_KEY` | JWT signing secret | `your-super-secret-key` |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Learning Resources

### Official Documentation
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/ (Start here!)
- **SQLAlchemy Tutorial**: https://docs.sqlalchemy.org/en/20/tutorial/
- **Pydantic Documentation**: https://docs.pydantic.dev/

### Helpful Tutorials
- FastAPI's own tutorial is excellent for beginners
- "FastAPI for Beginners" on YouTube
- Real Python's FastAPI articles

### Common Questions

**Q: Why do I get "database connection" errors?**
A: Make sure PostgreSQL is running and your DATABASE_URL in `.env` is correct.

**Q: What's the difference between Pydantic models and SQLAlchemy models?**
A: Pydantic models validate API data, SQLAlchemy models represent database tables.

**Q: How do I add more fields to my models?**
A: Add them to both the SQLAlchemy model (database) and Pydantic model (API validation).

**Q: Why use JWT tokens instead of sessions?**
A: JWT tokens are stateless, scalable, and work great with modern frontend frameworks.

### Getting Help
- Create an issue in this repository
- Ask on Stack Overflow with the `fastapi` tag
- Join the FastAPI Discord community
- Check the FastAPI GitHub discussions

### What to Build Next
- Todo API with user authentication
- E-commerce API with products and orders
- Social media API with posts and followers
- File upload API with image processing

Remember: The best way to learn is by building! Start with this project, understand how it works, then modify it to create something new. 🚀