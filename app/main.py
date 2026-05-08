from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="SHL Assessment Agent")

app.include_router(router)