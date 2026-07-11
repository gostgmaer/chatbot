from pathlib import Path


class PromptManager:
    def __init__(self):
        self.root = Path(__file__).resolve().parent.parent / "prompts"
        self.current = "default"

    def load(self, name: str) -> str:
        file = self.root / f"{name}.md"
        if not file.exists():
            raise FileNotFoundError(f"Prompt file not found: {file}")
        self.current = name
        return file.read_text(encoding="utf-8")

    def current_prompt(self):
        return self.load(self.current)

    def avaliable_prompts(self):
        return sorted(file.stem for file in self.root.glob("*.md"))

    def get_prompt(self, name: str) -> str:
        return self.load(name)
