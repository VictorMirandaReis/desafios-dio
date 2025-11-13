import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.config import settings
    from src.controllers import account, auth, transaction
    from src.database import database
    from src.exceptions import AccountNotFoundError, BusinessError
except ImportError:
    print("ERRO na importação de pacote!!")
    exit(1)


tags_metadata = [
    {
        "name": "auth",
        "description": "Operations for authentication.",
    },
    {
        "name": "account",
        "description": "Operations to maintain [accounts].",
        "externalDocs": {
            "description": "Doc. Accounts.api",
            "url": "https://account-api.com/",
        },
    },
    {
        "name": "transaction",
        "description": "Operations to maintain [transactions].",
        "externalDocs": {
            "description": "Doc. Transaction.api",
            "url": "https://transaction-api.com/",
        },
    },
]

servers = [
    {"url": "http://localhost:8000", "description": "Ambiente de desenvolvimento"},
    {
        "url": "https://dio-bank-package.onrender.com",
        "description": "Ambiente de produção",
    },
]


# pylint: disable=C0116
def create_app():
    # metadata.create_all(engine)

    # pylint: disable=W0621
    # pylint: disable=W0613
    @asynccontextmanager
    async def lifespan(app: FastAPI):  # noqa
        await database.connect()  # noqa
        yield
        await database.disconnect()  # noqa

    app_create_app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        summary=settings.SUMMARY,
        description="""
Transactions API is the microservice for recording current account transactions. 💸💰

## Account

* **Create accounts**.
* **List accounts**.
* **List account transactions by ID**.

## Transaction

* **Create transactions**.
""",
        openapi_tags=tags_metadata,
        servers=servers,
        redoc_url=None,
        # openapi_url=None, # disable docs
        lifespan=lifespan,
    )
    app_create_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app_create_app.include_router(auth.router, tags=["auth"])
    app_create_app.include_router(account.router, tags=["account"])
    app_create_app.include_router(transaction.router, tags=["transaction"])

    @app_create_app.exception_handler(AccountNotFoundError)
    async def account_not_found_error_handler(request: Request,
                                              exc: AccountNotFoundError
                                              ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Account not found."},
        )

    @app_create_app.exception_handler(BusinessError)
    async def business_error_handler(request: Request, exc: BusinessError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
        )

    return app_create_app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )
