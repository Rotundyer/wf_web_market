import uuid
import logging
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from sqlalchemy import delete, inspect, select
from sqlalchemy.orm import joinedload
# from sqlmodel import delete
from market_analysis.db.models import Order
from market_analysis.backstage.order_shema import Payload


class OrderDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_orders(self, payload: Payload, item_id: uuid.UUID, url_name: str) -> None:
        query = delete(Order).where(Order.item_id == item_id)
        await self.db_session.execute(query)

        orders: list[Order] = []

        for order in payload.payload.orders:
            orders.append(Order(
                item_id=item_id,
                order_id=order.id,
                url_name=url_name,
                platinum=order.platinum,
                quantity=order.quantity,
                order_type=order.order_type,
                rank=order.mod_rank,
                platform=order.platform,
                creation_date=order.creation_date,
                last_update=order.last_update,
                user_id=order.user.id,
                user_ingame_name=order.user.ingame_name,
                user_reputation=order.user.reputation,
                user_last_seen=order.user.last_seen,
                user_avatar=order.user.avatar
            ))

        await self.db_session.run_sync(lambda session: session.bulk_insert_mappings(Order, orders))

        print(f'Orders for subject \033[0;32m{url_name}\033[0m have been successfully uploaded to the database')

    async def get_all_orders(self) -> list[Order]:
        query = select(Order)
        res = await self.db_session.execute(query)
        rows = res.fetchall()
        orders: list[Order] = []
        for row in rows:
            for order in row:
                orders.append(order)
        return orders
