

from ui.cli import CLI
from services.chat_service import ChatService
from config.database import init_db

init_db()

ui = CLI()
service = ChatService()

ui.clear()
ui.banner()

chat = service.create_chat("New Chat")

while True:

    message = ui.user_input()

    if message == "/exit":
        break

    if message == "/help":
        ui.help()
        continue

    try:
        response = service.send_message(chat.id, message)
        ui.assistant_message(response)

    except Exception as e:
        ui.error(str(e))