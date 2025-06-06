from logging import getLogger

from fastapi import APIRouter, Depends

from app.lib.security import AccountSignInForm, JWTBearer


from .accounts import router as account_router
from .chat import router as chat_router
from .users import router as user_router
from .support import router as support_router

logger = getLogger(__name__)

root_router = APIRouter()

root_router.include_router(support_router)
root_router.include_router(account_router)
root_router.include_router(user_router)
root_router.include_router(chat_router)

test_router = APIRouter()


@test_router.get("/test")
async def default_test(auth_token=Depends(JWTBearer)):
    return {"test": str(auth_token)}


@test_router.get("/test2")
async def custom_test(auth_token=Depends(AccountSignInForm)):
    return {"test": str(auth_token)}


root_router.include_router(test_router)
