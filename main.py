from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.db import settings,create_table
from routers.routers import napp

app=FastAPI(
    title="Notes App",
    description="Api for Notes App",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
create_table()

app.include_router(napp,prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
