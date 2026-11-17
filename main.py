import time
from fastapi import FastAPI, Request
from routers import auth, guests, events, vendors, expenses, users
from fastapi.middleware import CORSMiddleware

app=FastAPI()

@app.middleware("http")
async def measure_request_time(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.6f} seconds"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Wedding Management API is running"}

app.include_router(guests.router)
app.include_router(events.router)
app.include_router(vendors.router)
app.include_router(expenses.router)
app.include_router(users.router)
app.include_router(auth.router)