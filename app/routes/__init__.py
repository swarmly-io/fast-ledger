from bank.persistence.database import DocumentDatabase
from bank.persistence.transactional_database import TransactionalDatabase

from fastapi.logger import logger

logger.warn("STARTING DB INSTANCES")
transactional = TransactionalDatabase()
documents = DocumentDatabase()
logger.warn("COMPLETED DB INSTANCES")