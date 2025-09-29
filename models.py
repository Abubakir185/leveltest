from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, BigInteger, Boolean
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_answers: Mapped[list["UserAnswer"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Level(Base):
    __tablename__ = "levels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    questions: Mapped[list["Question"]] = relationship(back_populates="level", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id", ondelete="CASCADE"))
    text: Mapped[str] = mapped_column(Text, nullable=False)
    option_a: Mapped[str] = mapped_column(String(255), nullable=False)
    option_b: Mapped[str] = mapped_column(String(255), nullable=False)
    option_c: Mapped[str] = mapped_column(String(255), nullable=False)
    option_d: Mapped[str] = mapped_column(String(255), nullable=False)
    correct_option: Mapped[str] = mapped_column(String(1), nullable=False)  

    level: Mapped["Level"] = relationship(back_populates="questions")
    user_answers: Mapped[list["UserAnswer"]] = relationship(back_populates="question", cascade="all, delete-orphan")


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete='CASCADE'))
    selected_option: Mapped[str] = mapped_column(String(1), nullable=False)
    is_correct: Mapped[bool] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="user_answers")
    question: Mapped["Question"] = relationship(back_populates="user_answers")


class Kanal(Base):
    __tablename__ = "kanallar"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    kanal_nomi: Mapped[str] = mapped_column(Text)
    kanal_id: Mapped[int] = mapped_column(BigInteger)
    kanal_url: Mapped[str] = mapped_column(Text)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    is_joined: Mapped[int] = mapped_column(Integer, default=0)
    user_count: Mapped[int] = mapped_column(Integer, default=0)
