# Wedding Management API

A backend REST API built with Python and FastAPI for managing wedding-related information such as guests, events, vendors, and expenses.

## Features

- Guest management
- Event management
- Vendor management
- Expense management
- CRUD operations
- Request and response validation using Pydantic
- SQLite database persistence
- SQLAlchemy ORM
- Automatic API documentation with Swagger UI
- HTTP status code and error handling

## Technologies

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn

## API Endpoints

### Guests

- POST /guests/
- GET /guests/
- GET /guests/{guest_id}
- PUT /guests/{guest_id}
- DELETE /guests/{guest_id}

### Events

- POST /events/
- GET /events/
- GET /events/{event_id}
- PUT /events/{event_id}
- DELETE /events/{event_id}

### Vendors

- POST /vendors/
- GET /vendors/
- GET /vendors/{vendor_id}
- PUT /vendors/{vendor_id}
- DELETE /vendors/{vendor_id}

### Expenses

- POST /expenses/
- GET /expenses/
- GET /expenses/{expense_id}
- PUT /expenses/{expense_id}
- DELETE /expenses/{expense_id}

## How to Run

### 1. Install dependencies

pip install fastapi uvicorn sqlalchemy pydantic

### 2. Start the server

uvicorn main:app --reload

### 3. Open Swagger UI

http://127.0.0.1:8000/docs

## Project Structure

FastAPI practice/
├── routers/
│   ├── guests.py
│   ├── events.py
│   ├── vendors.py
│   └── expenses.py
├── database.py
├── models.py
├── schemas.py
├── main.py
└── wedding.db