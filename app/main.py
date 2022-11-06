from app.database import Database
from bank.entity_models import Entity

from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from fastapi.logger import logger
from app.logger import init_logging
router = APIRouter(prefix='/api')
init_logging()

app = FastAPI()
@app.on_event("startup")
def startup_event():
    app.db = Database()
  
@router.post("/entity")
def create_entity(entity: Entity):
    couch = app.db.couch
    db = couch['test1'] if 'test1' in app.db.dbs else couch.create('test1')
    
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
app.include_router(router)