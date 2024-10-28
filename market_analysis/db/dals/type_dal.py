from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from market_analysis.db.models import Type, TypeCreate
from sqlmodel import select


class TypeDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_type(self, id: int):
        query = select(Type).where(Type.id == id)
        res = await self.db_session.execute(query)
        rows = res.fetchone()
        return rows
