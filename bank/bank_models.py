from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import Field, validator
from typing import List, Optional
from bank.id_basemodel import IdBaseModel

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
    
class Entity(IdBaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    company_name: Optional[str]
    company_description: Optional[str]
    address: Optional[str]
    account_number: Optional[str]
    bsb: Optional[str]
    account_id: Optional[UUID]
    entity_id: Optional[UUID]

class Transaction(IdBaseModel):
    description: Optional[str]
    date: datetime
    amount: Decimal
    currency: str
    account_id: UUID
    counter_party_entity_id: UUID
    reverse_approval: Optional[ReverseApproval]
    transaction_type: str

class Balances(IdBaseModel):
    currency: str
    amount: Decimal
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class Account(IdBaseModel):
    name: str
    details: BankDetails
    opened_date: datetime
    closed_date: Optional[datetime]
    
class IdDocument(IdBaseModel):
    type: str
    number: str
    country: str
    date_created: datetime
    verifier: str

class AccountEntity(IdBaseModel):
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
        return AccountEntity.name_must_be_non_empty(cls, v)
    
    def name_must_be_non_empty(cls, v):
        if not v or v == '':
            raise ValueError('No blank name')
        return v


     

    