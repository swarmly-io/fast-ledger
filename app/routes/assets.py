

from uuid import UUID
from fastapi import APIRouter
from bank.bank_models import Location, Valuation
from bank.ledger.assets_ledger import CreateAssetDto, AssetsLedger
from bank.ledger.base_ledger import IdDto
from . import documents, transactional, logger

router = APIRouter(prefix='/api', tags=["assets"])

@router.on_event("startup")
def startup():
    router.ledger = AssetsLedger(documents, transactional, logger)

@router.post("/asset/init")
def create_asset(assetDto: CreateAssetDto):
    return router.ledger.create_asset(assetDto.asset, assetDto.counter_party)

@router.post("/asset/valuation")
def add_valuation(valuation: Valuation):
    return router.ledger.add_valuation(valuation)

@router.post("/asset/location")
def add_valuation(location: Location):
    return router.ledger.add_location(location)

@router.post("/asset")
def get_asset(idDto: IdDto):
    return router.ledger.get_asset(idDto.id)