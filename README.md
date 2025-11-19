# Image Feed API

A modern image and video feed application built with FastAPI backend and Streamlit frontend.

## Project Structure

```
.
├── backend/                 # Backend application
│   └── app/
│       ├── __init__.py
│       ├── main.py         # FastAPI application entry point
│       ├── core/           # Core configuration and settings
│       │   ├── __init__.py
│       │   └── config.py   # Application settings
│       ├── db/             # Database configuration
│       │   ├── __init__.py
│       │   ├── base.py     # SQLAlchemy base
│       │   ├── session.py  # Database session management
│       │   ├── models.py   # Database models
│       │   └── init_db.py  # Database initialization
│       ├── models/         # Model exports (aliases)
│       │   └── __init__.py
│       ├── schemas/        # Pydantic schemas
│       │   ├── __init__.py
│       │   ├── user.py     # User schemas
│       │   └── post.py     # Post schemas
│       ├── api/            # API routes
│       │   ├── __init__.py
│       │   ├── deps.py     # API dependencies
│       │   └── v1/         # API version 1
│       │       ├── __init__.py
│       │       ├── auth.py    # Authentication endpoints
│       │       ├── users.py   # User endpoints
│       │       └── posts.py   # Post endpoints
│       ├── services/       # External services
│       │   ├── __init__.py
│       │   └── imagekit.py # ImageKit integration
│       └── users/          # User management
│           ├── __init__.py
│           └── manager.py  # User manager and auth
├── frontend/               # Frontend application
│   ├── __init__.py
│   └── app.py             # Streamlit application
├── tests/                  # Test files
│   ├── __init__.py
│   └── conftest.py        # Pytest configuration
├── main.py                # Application entry point
├── pyproject.toml         # Project dependencies
├── env.example            # Environment variables example
└── README.md              # This file
```

## Features

- **Authentication**: JWT-based user authentication
- **Image/Video Upload**: Upload images and videos with ImageKit integration
- **Feed**: View all posts in a feed format
- **User Management**: Register, login, and manage user accounts
- **Post Management**: Create, view, and delete posts

## Setup

### Prerequisites

- Python 3.13+
- ImageKit account (for file storage)
- `uv` package manager (recommended) or `pip`

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi-image-feed-api
```

2. Install dependencies:
```bash
uv sync
# or
pip install -e .
```

3. Create a `.env` file from `env.example`:
```bash
cp env.example .env
```

4. Update `.env` with your configuration:
```env
SECRET=your-secret-key-here
IMAGEKIT_PUBLIC_KEY=your-imagekit-public-key
IMAGEKIT_PRIVATE_KEY=your-imagekit-private-key
IMAGEKIT_URL_ENDPOINT=your-imagekit-url-endpoint
DATABASE_URL=sqlite+aiosqlite:///./image-feed.sqlite3
```

## Running the Application

### Backend (FastAPI)

```bash
python main.py
```

The API will be available at `http://localhost:8888`
API documentation: `http://localhost:8888/docs`

### Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

The frontend will be available at `http://localhost:8501`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/jwt/login` - Login and get JWT token
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/verify` - Verify email

### Users
- `GET /users/me` - Get current user info
- `PATCH /users/me` - Update current user

### Posts
- `POST /upload` - Upload an image or video
- `GET /feed` - Get all posts in feed
- `DELETE /post/{post_id}` - Delete a post

## Development

### Code Structure

The project follows best practices for FastAPI applications:

- **Separation of Concerns**: Clear separation between models, schemas, API routes, and services
- **Dependency Injection**: Using FastAPI's dependency system
- **Type Safety**: Using Pydantic for data validation
- **Async/Await**: Fully async database operations
- **Configuration Management**: Centralized settings with Pydantic Settings

### Adding New Features

1. **New API Endpoint**: Add to `backend/app/api/v1/`
2. **New Model**: Add to `backend/app/db/models.py`
3. **New Schema**: Add to `backend/app/schemas/`
4. **New Service**: Add to `backend/app/services/`

## License

See LICENSE file for details.

