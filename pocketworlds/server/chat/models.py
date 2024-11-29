from typing import Optional, List
from pydantic import BaseModel

class ChatBotRequest(BaseModel):
    user_message: str

class ChatBotResponse(BaseModel):
    """
    Initializes a ChatBotResponse object.

    :param system_response: The chatbot's response message
    :param supporting_urls: A list of URLs supporting the response, if any
    :param completed: A flag indicating whether the response successfully completed
    """
    system_response: str
    supporting_urls: Optional[List[str]] = []
    completed: bool

    def __str__(self):
        """
        String representation of the ChatBotResponse object, formatted as JSON-like output.
        """
        return (
            "{\n"
            f"    'response': '{self.system_response}',\n"
            f"    'supporting_urls': {self.supporting_urls if self.supporting_urls else []},\n"
            f"    'completed': {self.completed}\n"
            "}"
        )