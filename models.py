from datetime import datetime, UTC

from sqlalchemy import ForeignKey, String, ARRAY, JSON
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from database import Base


class User(Base):
    __tablename__ = "user_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    telegram_bots: Mapped[list["TelegramBot"]] = relationship(back_populates="user")


class TelegramUser(Base):
    __tablename__ = "telegram_user_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_user_id: Mapped[int] = mapped_column(unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    telegram_username: Mapped[str | None] = mapped_column(unique=True)

    survey_results: Mapped[list["SurveyResults"]] = relationship(
        back_populates="telegram_user"
    )

    def __repr__(self):
        return f"TelegramUser(id={self.id}, telegram_user_id={self.telegram_user_id}, username={self.telegram_username})"


class TelegramBot(Base):
    __tablename__ = "telegram_bot_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    latest_activity: Mapped[datetime] = mapped_column(default=None)
    active: Mapped[bool] = mapped_column(default=False)
    telegram_token: Mapped[str] = mapped_column(unique=True)
    internal_token: Mapped[str] = mapped_column(unique=True)
    survey: Mapped["Survey"] = relationship(back_populates="telegram_bot")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_table.id"),
        unique=True,
    )
    user: Mapped[User] = relationship(
        back_populates="telegram_bots",
        single_parent=True,
    )

    def __repr__(self):
        return f"TelegramBot(id={self.id}, name={self.name}, active={self.active}"


class Survey(Base):
    __tablename__ = "survey_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    questions: Mapped[list[str]] = mapped_column(ARRAY(String))
    greeting: Mapped[str | None]
    conclusion: Mapped[str | None]
    telegram_bot_id: Mapped[int | None] = mapped_column(
        ForeignKey("telegram_bot_table.id"),
        unique=True,
    )
    telegram_bot: Mapped[TelegramBot] = relationship(
        back_populates="survey",
        single_parent=True,
    )
    survey_results: Mapped[list["SurveyResults"]] = relationship(
        back_populates="survey"
    )


class SurveyResults(Base):
    __tablename__ = "survey_results_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    answers: Mapped[dict[str, str]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    survey_id: Mapped[int] = mapped_column(ForeignKey("survey_table.id"))
    survey: Mapped[Survey] = relationship(back_populates="survey_results")
    telegram_user_id: Mapped[int] = mapped_column(ForeignKey("telegram_user_table.id"))
    telegram_user: Mapped[TelegramUser] = relationship(back_populates="survey_results")
