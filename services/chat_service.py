from model.chat import Chat
from prompt_manager import PromptManager
from repository.chat import ChatRepository
from services.chatbot import GeminiChatbot

class ChatService:
    def __init__(self):
        self.repo = ChatRepository()
        self.bot = GeminiChatbot()
        self.prompt = PromptManager()

    def create_chat(self, title: str):
        return self.repo.create_chat(title=title)

    def send_message(self, chat_id: int, message: str):
        self.repo.add_message(chat_id=chat_id, role="user", content=message)
        history = self._build_history(chat_id=chat_id)
        response = self.bot.ask(history, self.prompt.system_prompt)
        self.repo.add_message(chat_id=chat_id, role="assistant", content=response.text)
        return response.text

    def _build_history(self, chat_id: int):
        history = []
        messages = self.repo.get_messages(chat_id=chat_id)
        # return [Message(role=msg.role, content=msg.content) for msg in messages]
        for message in messages:

            role = "user"

        if message.role == "assistant":
            role = "model"

        history.append({"role": role, "parts": [{"text": message.content}]})
        return history
