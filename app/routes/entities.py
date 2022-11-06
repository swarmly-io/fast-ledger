
from fastapi import APIRouter
from app.database import Database
from fastapi.logger import logger

from bank.entity_models import Entity

router = APIRouter(prefix='/api')

@router.on_event("startup")
def startup_event():
    router.db = Database()

@router.get("/entities")
def get_entities():
    couch = router.db.couch
    db = couch['test1'] if 'test1' in router.db.dbs else couch.create('test1')
    docs = db.get("_all_docs")['rows']
    logger.warn(docs)
    entities = [db.get(d['id']) for d in docs]
    return entities  

@router.post("/entity")
def create_entity(entity: Entity):
    couch = router.db.couch
    db = couch['test1'] if 'test1' in router.db.dbs else couch.create('test1')
    
    dbentity = Database.todict(entity)
    dbentity["_id"] = str(entity.id)
    existing = db.get(str(dbentity["_id"]))
    logger.warn(existing)
    if existing:
        logger.warn("Updating")
        dbentity['_rev'] = existing['_rev']
        db.save(dbentity)
    else:
        logger.warn("Creating")
        db.save(dbentity)
    return entity 