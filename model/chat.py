from sqlalchemy import DateTime,ForeignKey,Integer,Float,String,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship
from datetime import datetime
from config.database import BaseModel




class Chat(BaseModel):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True,autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False,default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False,default=datetime.now)
    title:Mapped[str]=mapped_column(String(5000),nullable=False)
    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat",
        cascade="all, delete-orphan",
        order_by="Message.id",
    )

class Message(BaseModel):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id"),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    chat: Mapped["Chat"] = relationship(
        back_populates="messages",
    )