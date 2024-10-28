from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import Union
from market_analysis.db.models import Item
from market_analysis.routers.response_model.item_model import ItemModel


class ItemDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_item(self, item_create: ItemModel, _type: int = 1) -> Union[Item, str]:
        query = select(Item).where(Item.wfm_id == item_create.wfm_id, Item.url_name == item_create.url_name)
        res = await self.db_session.execute(query)
        row = res.fetchone()
        if row is None:
            new_item = Item(
                wfm_id=item_create.wfm_id,
                url_name=item_create.url_name,
                trading_tax=item_create.trading_tax,
                icon=item_create.icon,
                type=_type
            )
            self.db_session.add(new_item)
            await self.db_session.commit()
            await self.db_session.refresh(new_item)
            print(new_item)
            return new_item
        return 'Such an item already exists in the database'

    async def get_all_items(self) -> list[Item]:
        query = select(Item)
        res = await self.db_session.execute(query)
        rows = res.fetchall()
        items: list[Item] = []
        for row in rows:
            for item in row:
                items.append(item)
        return items
