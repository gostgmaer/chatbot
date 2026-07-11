
from model.chat import Chat, Message


class ConversationManager:

    def __init__(self, max_messages: int = 20):

        self.max_messages = max_messages

    def build_history(self, messages: list[Message]):

        history = []

        recent = messages[-self.max_messages:]

        for message in recent:

            role = "user"

            if message.role == "assistant":
                role = "model"

            history.append(
                {
                    "role": role,
                    "parts": [
                        {
                            "text": message.content
                        }
                    ]
                }
            )

        return history