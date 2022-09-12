from abc import abstractmethod

from pydantic import BaseModel


class AbstractLoremaster(BaseModel):
    @abstractmethod
    def generate_event(self):
        """ """
