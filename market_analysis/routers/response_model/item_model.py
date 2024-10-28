import dataclasses
from typing import Optional
from pydantic import BaseModel
from pydantic.dataclasses import dataclass


class ItemModel(BaseModel):
    wfm_id: str
    url_name: str
    trading_tax: int
    icon: Optional[str] = None
    in_pool: Optional[bool] = False
