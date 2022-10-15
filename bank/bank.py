
from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from typing import List
from pydantic import BaseModel

from bank.entity import Entity

class Authority(str, Enum):
    CREATE_ENTITY = "Create an Entity"
    TRANSACT = "Perform a forward transaction"
    REVERSE_TRANSACTION = "Reverse a transaction"
    ADD_ACCOUNT = "Add account to existing entity"
    
class InternalEntity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    grants: List[Authority]

class Bank(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    entities: List[Entity]
    internal_entities: List[InternalEntity]