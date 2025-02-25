from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from telegram_bot.schemas import Update

router = APIRouter(prefix="/telegram_bot", tags=["telegram_bot"])


@router.post("/webhook/{bot_token}", status_code=status.HTTP_200_OK)
def webhook(bot_token: str, update: Update, db: Session = Depends(get_db)):
    pass
