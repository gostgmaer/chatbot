

from sqlalchemy import select
from config.database import get_session
from model.chat import Chat, Message


class ChatRepository:
    def create_chat(self, title: str) -> Chat:
        with get_session() as session:
            chat = Chat(title=title)
            session.add(chat)
            session.commit()
            session.refresh(chat)
            return chat

    def get_chat(self, chat_id: int) -> Chat:
        with get_session() as session:
            return session.get(Chat, chat_id)

    def list_chat(self) -> list[Chat]:
        with get_session() as session:
            stmt = select(Chat).order_by(Chat.created_at.desc())
            return list(session.scalars(stmt))

    def delete_chat(self, chat_id: int) -> int:
        with get_session() as session:
            chat = session.get(Chat, chat_id)
            if Chat is None:
                return False
            session.delete(chat)
            session.commit()
            return True

    def add_message(self, chat_id: int, role: str, content: str) -> Message:
        with get_session() as session:
            chat = session.get(Chat, chat_id)
            if not chat:
                return False
            message = Message(chat_id=chat_id, role=role, content=content)
            session.add(message)
            session.commit()
            session.refresh(message)
            return message

    def get_messages(self, chat_id: int) -> list[Message]:
        with get_session() as session:
            stmt = (
                select(Message)
                .where(Message.chat_id == chat_id)
                .order_by(Message.created_at)
            )
            return list(session.scalars(stmt))
