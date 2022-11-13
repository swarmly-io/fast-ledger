from app.routes import entities, transactions, bank

from fastapi import FastAPI, Response
from app.logger import init_logging

init_logging()

app = FastAPI(log_level="trace")

app.include_router(entities.router)
app.include_router(transactions.router)
app.include_router(bank.router)

# todo enable only in local env
@app.exception_handler(Exception)
def debug_exception_handler(request, exc: Exception):
    import traceback

    return Response(
        content="".join(
            traceback.format_exception(
                etype=type(exc), value=exc, tb=exc.__traceback__
            )
        )
    )