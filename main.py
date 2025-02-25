from contextlib import asynccontextmanager

from fastapi import FastAPI
from database import Base, engine
from telegram_bot.api import router as telegram_bot_router
from models import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(telegram_bot_router)
