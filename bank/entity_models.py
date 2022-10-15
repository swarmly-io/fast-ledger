from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import List, Optional

class Address(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    unit_floor: str
    building_name: str
    street_number: str
    street_name: str
    suburb: str
    post_zip_code: str
    country: str
    other: str

class PhoneNumber(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    prefix: str
    number: str
    extension: str
    
class BankDetails(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    bank_name: str
    bank_id: UUID
    bsb: str
    account_number: str     

class ReverseApproval(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    description: str
    approved: bool
    approvers: List[UUID]
    reference_transaction: UUID

class Transaction(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    description: str
    date: datetime
    amount: Decimal
    # todo currency: str
    counter_party: UUID
    reverse_approval: Optional[ReverseApproval]

class Account(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    details: BankDetails
    balance: Decimal
    balanceCurrency: str
    opened_date: datetime
    closed_date: datetime
    transactions: List[Transaction]
    
class IdDocument(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: str
    number: str
    country: str
    date_created: datetime
    verifier: str

class Entity(BaseModel):
    id: UUID  = Field(default_factory=uuid4)
    first_name: str
    middle_name: str
    last_name: str
    id_documents: List[IdDocument]
    place_of_birth: str
    addresses: List[Address]
    phone_numbers: List[PhoneNumber]
    accounts: List[Account]
    start_date: datetime
    end_date: datetime
     

    