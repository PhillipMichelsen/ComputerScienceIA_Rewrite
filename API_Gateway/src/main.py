import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.rest_router import router as rest_router
from src.api.webhook_router import router as webhook_router
from src.api.test_router import router as test_router

api = FastAPI()
api.include_router(rest_router)
api.include_router(test_router)
api.include_router(webhook_router)

# corms allow all
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s"
)


@api.get("/")
def read_root():
    return {"Working!"}


if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)
