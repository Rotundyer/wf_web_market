import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
from typing import Union
from market_analysis.db.models import ItemUpdate
from fastapi_cache.decorator import cache


class ItemUpdateDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_update(self, item_id: uuid.UUID, wfm_id: str, url_name: str) -> str:
        query = select(ItemUpdate).where(ItemUpdate.item_id == item_id)
        res = await self.db_session.execute(query)
        row = res.fetchone()
        if row is None:
            new_update = ItemUpdate(
                item_id=item_id,
                wfm_id=wfm_id,
                url_name=url_name
            )
            self.db_session.add(new_update)
            await self.db_session.commit()
            return f'Item with "item_id={item_id}" successfully added to the update pool'
        return 'An error occurred while trying to add an item to the update pool'

    async def get_all_updates(self) -> list[ItemUpdate]:
        updates: list[ItemUpdate] = []
        try:
            query = select(ItemUpdate)
            res = await self.db_session.execute(query)
            rows = res.fetchall()
            for row in rows:
                for item_update in row:
                    updates.append(item_update)
        except BaseException as e:
            print(e)
        finally:
            return updates
