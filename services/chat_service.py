from model.chat import Chat
from services.prompt_manager import PromptManager
from repository.chat import ChatRepository
from services.chatbot import GeminiChatbot
from tools.executor import ToolExecuter
from tools.registry import ToolRegistry
from google.genai import types


class ChatService:
    def __init__(self):
        self.repo = ChatRepository()
        self.bot = GeminiChatbot()
        self.prompt = PromptManager()
        self.registry = ToolRegistry()
        self.executor = ToolExecuter(self.registry)

    def create_chat(self, title: str):
        return self.repo.create_chat(title=title)

    def send_message(self, chat_id: int, message: str):
        self.repo.add_message(chat_id=chat_id, role="user", content=message)
        history = self._build_history(chat_id=chat_id)
        
        while True:
            response = self.bot.ask(
                history, 
                self.prompt.current_prompt(), 
                tools=self.registry.gemini_tools()
            )
            
            if response.function_calls:
                # Use the exact content from candidate to preserve thought_signature, etc.
                history.append(response.candidates[0].content)
                
                tool_parts = []
                for fc in response.function_calls:
                    try:
                        result = self.executor.execute(fc.name, **fc.args)
                    except Exception as e:
                        result = {"error": str(e)}
                    
                    if not isinstance(result, dict):
                        result = {"result": result}
                    
                    tool_parts.append(types.Part.from_function_response(name=fc.name, response=result))
                
                history.append(
                    types.Content(
                        role="tool",
                        parts=tool_parts
                    )
                )
                continue
            else:
                self.repo.add_message(chat_id=chat_id, role="assistant", content=response.text)
                return response.text

    def send_message_stream(self, chat_id: int, message: str):
        self.repo.add_message(chat_id=chat_id, role="user", content=message)
        history = self._build_history(chat_id=chat_id)
        
        while True:
            response_stream = self.bot.ask_stream(
                history, 
                self.prompt.current_prompt(), 
                tools=self.registry.gemini_tools()
            )
            
            function_calls = []
            parts = []
            full_response = []
            
            for chunk in response_stream:
                if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                    parts.extend(chunk.candidates[0].content.parts)
                    for part in chunk.candidates[0].content.parts:
                        if part.text:
                            full_response.append(part.text)
                            yield part.text
                if chunk.function_calls:
                    function_calls.extend(chunk.function_calls)
            
            if function_calls:
                # Reconstruct model content using all accumulated parts (retaining thought_signatures)
                history.append(
                    types.Content(
                        role="model",
                        parts=parts
                    )
                )
                
                tool_parts = []
                for fc in function_calls:
                    try:
                        result = self.executor.execute(fc.name, **fc.args)
                    except Exception as e:
                        result = {"error": str(e)}
                    
                    if not isinstance(result, dict):
                        result = {"result": result}
                    
                    tool_parts.append(types.Part.from_function_response(name=fc.name, response=result))
                
                history.append(
                    types.Content(
                        role="tool",
                        parts=tool_parts
                    )
                )
                continue
            else:
                self.repo.add_message(
                    chat_id=chat_id, role="assistant", content="".join(full_response)
                )
                break

    def _build_history(self, chat_id: int):
        history = []
        messages = self.repo.get_messages(chat_id=chat_id)
        for message in messages:
            role = "user"
            if message.role == "assistant":
                role = "model"
            history.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=message.content)]
                )
            )
        return history
