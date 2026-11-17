# Wedding Management API

A RESTful backend application built using **Python, FastAPI, and SQLAlchemy** to manage wedding-related information, including guests, events, vendors, and expenses.

The project demonstrates backend development concepts such as CRUD operations, relational database management, authentication, authorization, and centralized configuration.

## Features

- Guest management
- Event management
- Vendor management
- Vendor-to-event assignments
- Expense management
- CRUD operations
- SQLAlchemy ORM and relational database relationships
- Pydantic request and response validation
- JWT-based authentication
- Password hashing
- Role-based access control (RBAC)
- Admin user management
- Protected write operations
- Centralized application configuration
- Environment variable management
- Request processing time middleware
- CORS middleware
- Automatic API documentation using Swagger UI

## Technologies

- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- Pydantic Settings
- SQLite
- PyJWT
- pwdlib
- Uvicorn

## Authentication and Authorization

The application uses JWT (JSON Web Token) authentication.

- Users can register and log in.
- Passwords are hashed before being stored.
- Successful login generates an access token.
- Protected endpoints require a valid Bearer token.
- Role-based authorization distinguishes between regular users and administrators.
- Administrators can manage users and update their roles and account status.
- Inactive accounts cannot access protected resources.

### User Roles

| Role | Permissions |
|---|---|
| User | Access protected application write operations |
| Admin | User management and administrative operations, in addition to protected application operations |

## API Endpoints

### Authentication

| Method | Endpoint | Access |
|---|---|---|
| POST | `/auth/register` | Public |
| POST | `/auth/login` | Public |

### Users

| Method | Endpoint | Access |
|---|---|---|
| GET | `/users/me` | Authenticated |
| GET | `/users/` | Admin |
| PATCH | `/users/{user_id}/role` | Admin |
| PATCH | `/users/{user_id}/status` | Admin |

### Events

| Method | Endpoint | Access |
|---|---|---|
| POST | `/events/` | Authenticated |
| GET | `/events/` | Public |
| GET | `/events/{event_id}` | Public |
| GET | `/events/{event_id}/expenses` | Public |
| GET | `/events/{event_id}/guests` | Public |
| PUT | `/events/{event_id}` | Authenticated |
| PATCH | `/events/{event_id}` | Authenticated |
| DELETE | `/events/{event_id}` | Authenticated |

### Guests

| Method | Endpoint | Access |
|---|---|---|
| GET | `/guests/` | Public |
| POST | `/guests/` | Authenticated |
| GET | `/guests/{guest_id}` | Public |
| GET | `/guests/{guest_id}/events` | Public |
| POST | `/guests/{guest_id}/events/{event_id}` | Authenticated |
| PUT | `/guests/{guest_id}` | Authenticated |
| DELETE | `/guests/{guest_id}` | Authenticated |

### Vendors

| Method | Endpoint | Access |
|---|---|---|
| POST | `/vendors/` | Authenticated |
| POST | `/vendors/assign-event` | Authenticated |
| GET | `/vendors/` | Public |
| GET | `/vendors/{vendor_id}` | Public |
| GET | `/vendors/events/{event_id}/vendors` | Public |
| PUT | `/vendors/assignments/{assignment_id}/cost` | Authenticated |
| PUT | `/vendors/{vendor_id}` | Authenticated |
| DELETE | `/vendors/{vendor_id}` | Authenticated |
| DELETE | `/vendors/assignments/{assignment_id}` | Authenticated |

### Expenses

| Method | Endpoint | Access |
|---|---|---|
| POST | `/expenses/` | Authenticated |
| GET | `/expenses/` | Public |
| GET | `/expenses/total` | Public |
| GET | `/expenses/{expense_id}` | Public |
| PUT | `/expenses/{expense_id}` | Authenticated |
| DELETE | `/expenses/{expense_id}` | Authenticated |

**Access levels:** Public endpoints do not require authentication. Authenticated endpoints require a valid JWT Bearer token. Admin endpoints additionally require the administrator role.

**Note:** Application write operations require authentication. Administrative user-management endpoints require an admin role.

## Project Structure

```text
FastAPI practice/
│
├── routers/
│   ├── auth.py
│   ├── users.py
│   ├── guests.py
│   ├── events.py
│   ├── vendors.py
│   └── expenses.py
│
├── config.py
├── database.py
├── models.py
├── schemas.py
├── security.py
├── create_admin.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/nirupama-2503/WeddingManagementAPI.git
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Generate a secure JWT secret:

```powershell
$jwtSecret = python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Open `.env` and replace the placeholder for `JWT_SECRET_KEY` with the generated value.

The environment configuration includes:

```text
JWT_SECRET_KEY=your_generated_secret
DATABASE_URL=sqlite:///./wedding.db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not commit `.env` or expose your JWT secret.

### 5. Create the initial administrator account

```bash
python create_admin.py
```

Follow the prompts to create the administrator account.

### 6. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI provides interactive API documentation.

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

Use the Swagger UI to explore the available endpoints and interact with the API.

## Database

The application uses SQLite with SQLAlchemy ORM for database operations.

The database URL is configurable through environment variables. The default development database is `wedding.db`.

## Configuration and Security

- Application settings are centralized using Pydantic Settings.
- Sensitive configuration values are supplied through environment variables.
- JWT secrets are not stored in source code.
- Passwords are stored as hashes rather than plaintext.
- `.env` and database files are excluded from version control.

## Future Improvements

- Automated testing with Pytest
- Pagination, filtering, and sorting
- Background tasks
- File uploads
- Logging and monitoring
- Docker support
- Deployment
