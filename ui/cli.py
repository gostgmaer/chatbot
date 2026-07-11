"""
===============================================================
EasyDev AI - CLI User Interface
===============================================================

Purpose
-------
This module contains ONLY the presentation layer.

Responsibilities
----------------
✓ Display banners
✓ Display menus
✓ Read user input
✓ Display streamed AI responses
✓ Display loading spinner
✓ Display chat history
✓ Display success/error messages
✓ Confirm dangerous actions

DO NOT
------
✗ Call Gemini API
✗ Access SQLite
✗ Execute SQL
✗ Build prompts
✗ Execute business logic

Flow
----
User
    ↓
CLI
    ↓
ChatService
    ↓
Repository / Gemini
    ↓
CLI

===============================================================
"""

import shutil

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.markdown import Markdown
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.status import Status
from rich.text import Text

console = Console()
width = shutil.get_terminal_size().columns


class CLI:

    def __init__(self):
        self.console = console

    # ==========================================================
    # General
    # ==========================================================

    def clear(self):
        self.console.clear()

    def banner(self):

        self.console.print()

        self.console.print(
            Panel(
                Align.center(
                    "[bold cyan]🤖 EasyDev AI Assistant[/bold cyan]\n"
                    "[grey70]Powered by Gemini[/grey70]"
                ),
                title="[bold]EasyDev AI[/bold]",
                border_style="cyan",
                padding=(1, 4),
                expand=True,
            )
        )

        self.console.print("[grey70]Type /help for commands • /exit to quit[/grey70]\n")

    # ==========================================================
    # Menu
    # ==========================================================

    def menu(self):

        table = Table(
            title="Main Menu", show_header=False, border_style="cyan", width=width
        )

        table.add_column()
        table.add_column()

        table.add_row("1", "New Chat")
        table.add_row("2", "Continue Chat")
        table.add_row("3", "List Chats")
        table.add_row("4", "Delete Chat")
        table.add_row("5", "Rename Chat")
        table.add_row("6", "Settings")
        table.add_row("0", "Exit")

        self.console.print(table)

    def menu_choice(self):

        return Prompt.ask(
            "[bold cyan]Select[/bold cyan]",
            default="1",
        )

    # ==========================================================
    # Chat
    # ==========================================================

    def show_chat_header(self, title):

        self.console.print()

        self.console.print(Rule(f"[bold cyan]{title}[/bold cyan]"))

    def user_input(self):

        self.console.print("\n[bold green]👤 You[/bold green]")

        return Prompt.ask("[green]❯[/green]")

    def assistant_header(self):

        self.console.print("\n[bold blue]🤖 EasyDev AI[/bold blue]")

    def assistant_message(self, text):

        self.assistant_header()

        self.console.print(Markdown(text))

        self.console.print()

    # ==========================================================
    # Streaming
    # ==========================================================

    def stream_response(self, stream):
        self.assistant_header()

        with self.console.status(
            "[cyan]Thinking...[/cyan]",
            spinner="dots",
        ):
            iterator = iter(stream)
            try:
                first_chunk = next(iterator)
            except StopIteration:
                return

        def get_text(chunk):
            if isinstance(chunk, str):
                return chunk
            return getattr(chunk, "text", "") or ""

        text = get_text(first_chunk)
        if text:
            self.console.print(text, end="", soft_wrap=True)

        for chunk in iterator:
            text = get_text(chunk)
            if text:
                self.console.print(text, end="", soft_wrap=True)

        self.console.print("\n")

    # ==========================================================
    # Loading
    # ==========================================================

    def loading(self, text="Thinking..."):

        return Status(
            f"[cyan]{text}[/cyan]",
            console=self.console,
        )

    # ==========================================================
    # Notifications
    # ==========================================================

    def success(self, message):

        self.console.print(f"[bold green]✓ {message}[/bold green]")

    def warning(self, message):

        self.console.print(f"[bold yellow]! {message}[/bold yellow]")

    def error(self, message):

        self.console.print(f"[bold red]✗ {message}[/bold red]")

    # ==========================================================
    # Confirmation
    # ==========================================================

    def confirm(self, text):

        return Confirm.ask(text)

    # ==========================================================
    # Chats
    # ==========================================================

    def show_chats(self, chats):

        table = Table(
            title="Chats",
            border_style="cyan",
        )

        table.add_column("ID")
        table.add_column("Title")
        table.add_column("Created")

        for chat in chats:

            table.add_row(
                str(chat.id),
                chat.title,
                str(chat.created_at),
            )

        self.console.print(table)

    # ==========================================================
    # Messages
    # ==========================================================

    def show_history(self, messages):

        self.console.print()

        for message in messages:

            if message.role == "user":

                self.console.print("[bold green]👤 You[/bold green]")

            else:

                self.console.print("[bold blue]🤖 EasyDev[/bold blue]")

            self.console.print(Markdown(message.content))

            self.console.print(Rule(style="grey35"))

    # ==========================================================
    # Help
    # ==========================================================

    def help(self):

        table = Table(
            title="Commands",
            border_style="cyan",
        )

        table.add_column("Command")
        table.add_column("Description")

        table.add_row("/help", "Show help")
        table.add_row("/new", "New chat")
        table.add_row("/list", "List chats")
        table.add_row("/history", "Show history")
        table.add_row("/rename", "Rename current chat")
        table.add_row("/delete", "Delete current chat")
        table.add_row("/clear", "Clear terminal")
        table.add_row("/exit", "Exit application")

        self.console.print(table)
