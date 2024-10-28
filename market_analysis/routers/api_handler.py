import json

import requests
from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union
from market_analysis.settings import API_VERSION
from market_analysis.db.session import sessionmanager
from market_analysis.db.models import ArcaneLocationCreate, ArcaneLocation, Arcane
from market_analysis.db.dals.arcane_location_dal import ArcaneLocationDAL
from market_analysis.db.dals.item_dal import ItemDAL
from market_analysis.db.dals.arcane_dal import ArcaneDAL
from market_analysis.db.dals.item_update_dal import ItemUpdateDAL
from market_analysis.routers.response_model.arcane_model import ArcaneModel, ArcaneModelCreate
from market_analysis.routers.response_model.item_model import ItemModel
from market_analysis.db.models import ItemCreate

router = APIRouter(
    prefix=f"/api/{API_VERSION}",
    tags=['TradeWARF']
)


@router.post('/add_arcane_location', response_model=Union[ArcaneLocation, str], response_model_exclude_defaults=True)
async def set_arcane_location(location: ArcaneLocationCreate) -> Union[ArcaneLocation, str]:
    async with sessionmanager.session() as session:
        arcane_location_dal = ArcaneLocationDAL(session)
        return await arcane_location_dal.create_location(location)


@router.post('/get_item_from_wfm', response_model=Union[ArcaneModel, str], response_model_exclude_defaults=True)
async def get_item_from_wfm(url: str) -> Union[ArcaneModel, str]:
    try:
        response = requests.get(f'https://api.warframe.market/v1/items/{url}')
        data = response.json()['payload']['item']
        arcane = ArcaneModel(
            wfm_id=data['id'],
            url_name=url,
            trading_tax=data['items_in_set'][0]['trading_tax'],
            icon=data['items_in_set'][0]['icon'],
            max_rank=data['items_in_set'][0]['mod_max_rank'],
            in_pool=None,
            type=None
        )
        return arcane
    except:
        return 'The server was unable to process the request'


@router.post('/create_item', response_model=Union[Arcane, str], response_model_exclude_defaults=True)
async def create_arcane(arcane: ArcaneModelCreate,
                        _session: AsyncSession = Depends(sessionmanager.session)) -> Union[Arcane, str]:
    try:
        async with _session as session:
            item_dal = ItemDAL(session)
            item = await item_dal.create_item(arcane)
            item_id = item.item_id
            wfm_id = item.wfm_id
            url_name = item.url_name
            if type(item) is not str:
                arcane_dal = ArcaneDAL(session)
                arc = await arcane_dal.create_arcane(arcane, item_id=item_id)

                if arcane.in_pool:
                    item_update_dal = ItemUpdateDAL(session)
                    res_update = await item_update_dal.create_update(item_id=item_id,
                                                                     wfm_id=wfm_id,
                                                                     url_name=url_name)

                return arc
            else:
                return item
    except Exception as e:
        print(e)
        return 'An error occurred while recording an item'
