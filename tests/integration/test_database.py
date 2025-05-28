from logging import getLogger
from typing import Literal

import pytest
from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

logger = getLogger(__name__)
pytestmark = pytest.mark.asyncio


async def get_migraion_version(session: AsyncSession):
    try:
        return await session.execute(text("select version from alembic_version;"))
    except Exception as err:
        logger.error(err)
        return Literal["0"]


async def test_database_connection(engine: AsyncEngine, sessionmaker: async_sessionmaker[AsyncSession]):
    current_migration = await get_migraion_version(sessionmaker())
    logger.debug(current_migration)

    async with engine.begin() as conn:
        tables = await conn.run_sync(lambda c: inspect(c).get_table_names())
        logger.debug(tables)

    async with sessionmaker() as s, s.begin():
        res = await s.execute(text("select email from user_accounts limit 10;"))
        logger.debug(res.all())
        res = await s.execute(text("select title from chats limit 10;"))
        logger.debug(res.all())
        await s.rollback()

    async with sessionmaker() as session, session.begin():
        res = await session.execute(
            text("""
            SELECT user_accounts.id, user_accounts.email, user_accounts.hashed_password,
                chats.title, chats.kind, chats.creator_id, chats.id AS id_1 
            FROM user_accounts JOIN chats AS chats ON user_accounts.id = chats.creator_id 
            """)
        )
        logger.debug(str(res.fetchall()))
        await session.rollback()
