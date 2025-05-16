from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession


async def check_database(session: AsyncSession):
    try:
        await session.execute(text("SELECT 1"))
    except Exception:
        return "fail"

    return "ok"
