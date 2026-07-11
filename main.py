

from ui.cli import CLI
from services.chat_service import ChatService
from config.database import init_db

init_db()

ui = CLI()
service = ChatService()

ui.clear()
ui.banner()
ui.console.print(f"[dim]System prompt loaded: {service.prompt.current}[/dim]\n")

chat = service.create_chat("New Chat")

while True:

    message = ui.user_input()

    if message == "/exit":
        break

    if message == "/help":
        ui.help()
        continue

    if message.startswith("/prompt"):
        parts = message.split()
        if len(parts) > 1:
            prompt_name = parts[1]
            try:
                service.prompt.load(prompt_name)
                ui.success(f"Successfully loaded prompt: '{prompt_name}'")
            except Exception as e:
                ui.error(f"Failed to load prompt: {str(e)}")
        else:
            ui.console.print(f"\n[bold cyan]Active Prompt:[/bold cyan] {service.prompt.current}")
            available = service.prompt.avaliable_prompts()
            ui.console.print(f"[bold cyan]Available Prompts:[/bold cyan] {', '.join(available)}")
            from rich.panel import Panel
            ui.console.print(Panel(service.prompt.current_prompt(), title="Prompt Content", border_style="cyan"))
        continue

    try:
        response_stream = service.send_message_stream(chat.id, message)
        ui.stream_response(response_stream)

    except Exception as e:
        ui.error(str(e))