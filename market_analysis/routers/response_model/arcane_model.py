import dataclasses

from pydantic import BaseModel
from typing import Optional
from market_analysis.routers.response_model.item_model import ItemModel


class ArcaneModel(ItemModel):
    max_rank: int
    vosfor: Optional[int] = None
    reputation: Optional[int] = None


class ArcaneModelCreate(ArcaneModel):
    location: int
