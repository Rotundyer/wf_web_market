import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import Union
from market_analysis.db.models import Arcane
from market_analysis.routers.response_model.arcane_model import ArcaneModelCreate


class ArcaneDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_arcane(self, arcane_create: ArcaneModelCreate, item_id: uuid.UUID) -> Union[Arcane, str]:
        query = select(Arcane).where(Arcane.item_id == item_id)
        res = await self.db_session.execute(query)
        row = res.fetchone()
        if row is None:
            new_arcane = Arcane(
                item_id=item_id,
                max_rank=arcane_create.max_rank,
                location=arcane_create.location,
                vosfor=arcane_create.vosfor,
                reputation=arcane_create.reputation
            )
            self.db_session.add(new_arcane)
            await self.db_session.commit()
            await self.db_session.refresh(new_arcane)
            return new_arcane

        return 'Error with UUID duplication'
