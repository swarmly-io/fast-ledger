
from dataclasses import Field
from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel
from bank.entity_models import Transaction

class LedgerEntry(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    transaction: Transaction
    date_entered: datetime
    
class Ledger(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    entries: List[LedgerEntry]
    
