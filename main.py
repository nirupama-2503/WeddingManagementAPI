from fastapi import FastAPI
from routers import guests, events, vendors, expenses

app=FastAPI()

@app.get("/")
def home():
    return {"message": "Wedding Management API is running"}

app.include_router(guests.router)
app.include_router(events.router)
app.include_router(vendors.router)
app.include_router(expenses.router)

