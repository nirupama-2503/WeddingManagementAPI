
import time
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, guests, events, vendors, expenses, users
from logging_config import setup_logging


setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Wedding Management API is starting")
    yield
    logger.info("Wedding Management API is shutting down")


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def measure_request_time(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    response.headers["X-Process-Time"] = f"{process_time:.6f} seconds"

    logger.info(
        "%s %s - Status: %s - Processing time: %.6f seconds",
        request.method,
        request.url.path,
        response.status_code,
        process_time
    )

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
    logger.info("Home endpoint accessed")
    return {"message": "Wedding Management API is running"}


app.include_router(guests.router)
app.include_router(events.router)
app.include_router(vendors.router)
app.include_router(expenses.router)
app.include_router(users.router)
app.include_router(auth.router)
