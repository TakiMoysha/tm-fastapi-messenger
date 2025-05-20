from logging import getLogger
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = getLogger(__name__)


async def check_database(session: AsyncSession):
    try:
        await session.execute(text("SELECT 1"))
    except Exception as err:
        logger.exception(err)
        return "fail"

    return "ok"
