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

    def send_message_stream(self, chat_id: int, message: str):
        self.repo.add_message(chat_id=chat_id, role="user", content=message)
        history = self._build_history(chat_id=chat_id)
        response_stream = self.bot.ask_stream(history, self.prompt.system_prompt)
        
        full_response = []
        for chunk in response_stream:
            if chunk.text:
                full_response.append(chunk.text)
            yield chunk
            
        self.repo.add_message(chat_id=chat_id, role="assistant", content="".join(full_response))

    def _build_history(self, chat_id: int):
        history = []
        messages = self.repo.get_messages(chat_id=chat_id)
        for message in messages:
            role = "user"
            if message.role == "assistant":
                role = "model"
            history.append({"role": role, "parts": [{"text": message.content}]})
        return history
