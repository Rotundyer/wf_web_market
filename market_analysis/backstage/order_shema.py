from pydantic import BaseModel, field_validator
from enum import Enum
from datetime import datetime


class Status(str, Enum):
    ingame = 'ingame'
    online = 'online'
    offline = 'offline'


class OrderType(str, Enum):
    sell = 'sell'
    buy = 'buy'


class Platform(str, Enum):
    xbox = 'xbox'
    pc = 'pc'
    ps4 = 'ps4'
    switch = 'switch'


class User(BaseModel):
    id: str
    ingame_name: str
    status: Status
    region: str
    reputation: int
    avatar: str | None
    last_seen: datetime | None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Order(BaseModel):
    id: str
    platinum: int
    quantity: int
    order_type: OrderType
    platform: Platform
    region: str | None
    creation_date: datetime
    last_update: datetime | None
    subtype: str | None = None
    visible: bool
    user: User
    mod_rank: int

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Orders(BaseModel):
    orders: list[Order]


class Payload(BaseModel):
    payload: Orders