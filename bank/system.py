
from decimal import Decimal
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import List
from bank import Bank

class BankLinks(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    source: Bank
    target: Bank
    transaction_cost: Decimal

class System(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    banks: List[Bank]
    links: List[BankLinks]