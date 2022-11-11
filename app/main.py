from app.routes import entities, transactions, bank

from fastapi import FastAPI
from app.logger import init_logging
init_logging()

app = FastAPI()

app.include_router(entities.router)
app.include_router(transactions.router)
app.include_router(bank.router)