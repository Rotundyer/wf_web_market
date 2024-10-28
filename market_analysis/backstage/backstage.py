import asyncio
import requests
from market_analysis.db.session import sessionmanager
from market_analysis.db.dals.item_update_dal import ItemUpdateDAL
from market_analysis.db.dals.order_dal import OrderDAL
from market_analysis.backstage.order_shema import Payload


class BackstageRunner:
    def __init__(self):
        pass

    async def update_orders(self):
        await asyncio.sleep(10)
        async with sessionmanager.session() as session:
            item_update_dal = ItemUpdateDAL(session)
            order_dal = OrderDAL(session)
            while True:
                updates = await item_update_dal.get_all_updates()
                for item in updates:
                    try:
                        response = requests.get(f'https://api.warframe.market/v1/items/{item.url_name}/orders')
                        data = response.json()

                        await order_dal.add_orders(Payload(**data), item.item_id, url_name=item.url_name)
                    except Exception as e:
                        print(e)
                        continue

                await session.commit()

                await asyncio.sleep(60)
