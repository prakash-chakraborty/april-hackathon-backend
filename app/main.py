from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import health, users, pages, cards

app = FastAPI(title="Retail Copilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(users.router, prefix="/api")
app.include_router(pages.router, prefix="/api")
app.include_router(cards.router, prefix="/api")
