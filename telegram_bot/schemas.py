from pydantic import BaseModel, Field


class User(BaseModel):
    telegram_user_id: int = Field(alias="id")
    first_name: str
    last_name: str = None
    username: str = None


class Chat(BaseModel):
    telegram_chat_id: int = Field(alias="id")


class Message(BaseModel):
    message_id: int
    sender: User = Field(alias="from")
    date: int
    chat: Chat
    text: str = None


class CallbackQuery(BaseModel):
    message_id: int = Field(alias="id")
    sender: User = Field(alias="from")
    data: str = None


class Update(BaseModel):
    update_id: int
    message: Message = None
    edited_message: Message = None
    callback_query: CallbackQuery = None
