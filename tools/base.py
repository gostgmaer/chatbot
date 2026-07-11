from abc import ABC
from abc import abstractmethod
from google.genai import types


class BaseTool(ABC):
    """
    Base class for every tool.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique tool name.
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Tool description shown to the LLM.
        """
        pass

    @property
    @abstractmethod
    def schema(self) -> dict:
        """
        JSON schema describing the tool.
        """
        pass
    @property
    def declaration(self):

        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters_json_schema=self.schema,
        )
    @abstractmethod
    def execute(self, **kwargs):
        """
        Execute the tool.
        """
        pass