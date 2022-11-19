

from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import update
from bank.bank_models import Asset, Entity, Location, Valuation
from bank.ledger.base_ledger import BaseLedger
from bank.ledger.ledger_models import AssetEntry, EntityEntry, TransactionEntry
from bank.persistence.database import Buckets

class CreateAssetDto(BaseModel):
    asset: Asset
    counter_party: Entity
    
class AssetsLedger(BaseLedger):
    def create_asset(self, asset: Asset, counter_party: Entity):
        # create asset entry
        bucket = self.get_db(Buckets.ASSETS.value)
        entity_bucket = self.get_db(Buckets.ENTITIES.value)
        entity = entity_bucket.get(str(counter_party.id))
        if not entity:
            entity_bucket.save(counter_party)
        
        asset = bucket.get(str(asset.id))
        if asset:
            raise Exception("Asset with that id already exists")
        bucket.save(asset)
        with self.transactional.get_session() as session:
            # create transaction entry
            transaction = TransactionEntry(description="Asset added: " + asset.name, account_id=asset.account_id, transaction_type="ASSET", amount=asset.value, currency=asset.currency)            
            session.add(transaction)
            if not entity:
                entity_entry = EntityEntry(entity_id=counter_party.id)
                session.add(entity_entry)
            session.commit()
        
    def add_location(self, location: Location):
        location_bucket = self.get_db(f'{Buckets.LOCATIONS.value}_{location.asset_id}')
        location_bucket.save(location)
    
    # todo when a new valuation is entered, create a transaction for the difference between last valuation and this valuation
    def add_valuation(self, valuation: Valuation):
        valuation_bucket = self.get_db(f'{Buckets.VALUATIONS.value}_{valuation.asset_id}')
        valuation_bucket.save(valuation)
        
    def update_last_entries(self, asset_id: UUID):
        valuation = self.documents.get_last_id(f'{Buckets.VALUATIONS.value}_{asset_id}')
        location = self.documents.get_last_id(f'{Buckets.LOCATIONS.value}_{asset_id}')
        with self.transactional.get_session() as session:
            session.execute(
                update(AssetEntry).
                where(AssetEntry.asset_id == asset_id).
                values(recent_location_id=location, valuation_id=valuation)
            )
            
    def get_asset(self, asset_id: UUID):
        bucket = self.get_db(Buckets.ASSETS.value)
        return bucket.get(str(asset_id))
            
    def value_asset(self):
        pass