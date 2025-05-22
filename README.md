# Tasks Manager App 📋

A modern web application for task management built with FastAPI, React, PostgreSQL, and Docker. Allows users to create, manage, and track their tasks with a complete authentication and authorization system.

## Features

### User Management

- User registration and login
- JWT-based authentication
- User profiles with personal information
- Secure password updates
- Superuser roles for administration
- Account deletion

### Task Management

- Complete CRUD operations for tasks
- Task statuses: Pending, In Progress, Completed, Suspended
- Private tasks per user (each user sees only their tasks)
- Pagination and filtering
- Superusers can view all tasks

### Security

- JWT authentication with secure tokens
- Password hashing with bcrypt
- Data validation with Pydantic
- Role-based access control

## Tech Stack

### Backend

- **FastAPI** - Modern, fast web framework for Python
- **SQLModel** - Modern ORM with static typing
- **PostgreSQL** - Robust relational database
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **JWT** - Token-based authentication

### Frontend

- **React** - JavaScript library for building user interfaces
- **TypeScript** - JavaScript with static typing
- **Vite** - Modern build tool and dev server
- **Chakra UI** - Modular and accessible component library
- **React Hooks** - Modern React patterns for state management

### DevOps

- **Docker** - Containerization
- **Docker Compose** - Container orchestration
- **PostgreSQL** - Containerized database

## Installation and Setup

### Prerequisites

- Docker and Docker Compose installed
- Git
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Quick Setup with Docker

1. **Clone the repository**

   ```bash
   git clone https://github.com/Jamova01/task-manager-app.git
   cd task-manager-app
   ```

2. **Set up environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file with your configurations:

   ```env
   # Database
   POSTGRES_SERVER=db
   POSTGRES_PORT=5432
   POSTGRES_DB=tasks_manager
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=changethis

   # Security
   SECRET_KEY=your-super-secure-secret-key-here
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # First superuser
   FIRST_SUPERUSER=admin@example.com
   FIRST_SUPERUSER_PASSWORD=changethis
   ```

### Development Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Run with Docker Compose**

```bash
sudo docker compose up --build
```

**Access the application**

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Project Structure

```
task-manager-app/
├── backend/
│   ├── app/
│   │   ├── auth/           # Authentication and security
│   │   ├── models.py       # SQLModel data models
│   │   ├── services/       # Business logic
│   │   │   ├── user_service.py
│   │   │   └── task_service.py
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configuration
│   │   └── main.py         # FastAPI entry point
│   ├── alembic/            # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Application pages
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API services
│   │   └── utils/          # Utilities
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🔌 API Endpoints

### Authentication

- `POST /api/v1/login/access-token` - Login

### Users

- `GET /api/v1/users/` - List users (superuser only)
- `POST /api/v1/users/`- Create a new use (superuser only)
- `POST /api/v1/users/signup` - Register User
- `GET /api/v1/users/{user_id}` - Ger user details
- `PATCH /api/v1/users/{user_id}` - Update User
- `DELETE /api/v1/users/{user_id}` - Delete a User
- `GET /api/v1/users/me` - Get current profile
- `PUT /api/v1/users/me` - Update profile
- `DELETE /api/v1/users/me` - Delete account

### Tasks

- `GET /api/v1/tasks/` - List user tasks
- `POST /api/v1/tasks/` - Create task
- `GET /api/v1/tasks/{task_id}` - Get specific task
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task

## 📊 Data Models

### User

```python
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "Full Name",
  "is_active": true,
  "is_superuser": false
}
```

### Task

```python
{
  "id": "uuid",
  "title": "Task title",
  "description": "Optional description",
  "status": "pending|in_progress|completed|suspended",
  "owner_id": "uuid"
}
```

## 🧪 Testing

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npm test
```

## Production Deployment

### With Docker

```bash
# Build production images
sudo docker-compose -f docker-compose.prod.yml build

# Deploy
sudo docker-compose -f docker-compose.prod.yml up -d
```

### Production Environment Variables

- Change `SECRET_KEY` to a unique secure key
- Set `POSTGRES_PASSWORD` with a strong password
- Configure `FIRST_SUPERUSER` and `FIRST_SUPERUSER_PASSWORD`
- Set up appropriate domains and CORS settings

## 🔧 Useful Commands

### Docker

```bash
# View logs
sudo docker compose logs -f

# Restart services
sudo docker compose restart

# Clean volumes
sudo docker compose down -v
```

### Database

```bash
# Create new migration
alembic revision --autogenerate -m "change description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🙋‍♂️ Support

Have questions or issues?

- 📧 Email: jorgemova01@gmail.com

---
