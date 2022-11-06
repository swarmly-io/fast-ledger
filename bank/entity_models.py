from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class IdBaseModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)

class Address(IdBaseModel):
    unit_floor: str
    building_name: str
    street_number: str
    street_name: str
    suburb: str
    post_zip_code: str
    country: str
    other: str

class PhoneNumber(IdBaseModel):
    prefix: str
    number: str
    extension: str
    
class BankDetails(IdBaseModel):
    bank_name: str
    bank_id: UUID
    bsb: str
    account_number: str     

class ReverseApproval(IdBaseModel):
    description: str
    approved: bool
    approvers: List[UUID]
    reference_transaction: UUID

class Transaction(IdBaseModel):
    description: str
    date: datetime
    amount: Decimal
    # todo currency: str
    counter_party: UUID
    reverse_approval: Optional[ReverseApproval]

class Account(IdBaseModel):
    name: str
    details: BankDetails
    balance: Decimal
    balanceCurrency: str
    opened_date: datetime
    closed_date: Optional[datetime]
    transactions: List[Transaction]
    
class IdDocument(IdBaseModel):
    type: str
    number: str
    country: str
    date_created: datetime
    verifier: str

class Entity(IdBaseModel):
    first_name: str 
    middle_name: str
    last_name: str
    id_documents: List[IdDocument]
    place_of_birth: str
    addresses: List[Address]
    phone_numbers: List[PhoneNumber]
    accounts: List[Account]
    created_date: datetime = Field(default_factory=datetime.utcnow)
    closed_date: Optional[datetime]
    
    @validator('first_name')
    def first_name_validator(cls, v):
        return Entity.name_must_be_non_empty(cls, v)
    
    def name_must_be_non_empty(cls, v):
        if not v or v == '':
            raise ValueError('No blank name')
        return v
    

     

    