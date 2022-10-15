
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from typing import List
from pydantic import BaseModel

from bank.entity import Entity

class Bank(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    entities: List[Entity]