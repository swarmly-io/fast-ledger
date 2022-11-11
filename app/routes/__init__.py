from bank.persistence.database import Database
from bank.persistence.transactional_database import TransactionalDatabase

from fastapi.logger import logger

logger.warn("STARTING DB INSTANCES")
transactional = TransactionalDatabase()
documents = Database()
logger.warn("COMPLETED DB INSTANCES")