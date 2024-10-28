import uuid
from typing import Optional, List, Dict
from datetime import datetime
from pydantic.dataclasses import dataclass
from sqlmodel import Column
from sqlmodel import (
    SQLModel,
    Field,
    String,
    ARRAY,
    SmallInteger,
    Integer,
    Text,
    DateTime,
    UUID
)


# Item
class ItemBase(SQLModel):
    wfm_id: str
    url_name: str
    trading_tax: Optional[int]
    icon: Optional[str]
    type: int


class Item(ItemBase, table=True):
    __tablename__ = 'items'
    item_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False,
                               description='Main id')
    wfm_id: str = Field(sa_column=Column(String(63), nullable=False, unique=True),
                        description='Warframe market item id')
    url_name: str = Field(sa_column=Column(String(63), nullable=False, unique=True), description='Warframe market url')
    trading_tax: Optional[int] = Field(default=None, nullable=True, description='Trade tax')
    icon: Optional[str] = Field(default=None, sa_column=Column(String(255), nullable=True),
                                description='Warframe market icon')
    type: int = Field(nullable=False, foreign_key='types.id',
                      description='Classification of an object according to its purpose')


class ItemCreate(ItemBase):
    pass


# Arcanes
class ArcaneBase(SQLModel):
    item_id: uuid.UUID
    max_rank: Optional[int]
    location: Optional[str]
    vosfor: Optional[int]
    reputation: Optional[int]


class Arcane(ArcaneBase, table=True):
    __tablename__ = 'arcanes'
    item_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False,
                               foreign_key='items.item_id')
    max_rank: Optional[int] = Field(default=None, sa_column=Column(SmallInteger, nullable=True),
                                    description='Maximum possible Arcane rank')
    location: Optional[int] = Field(default=None, sa_column=Column(SmallInteger, nullable=True),
                                    description='The place where the arcane is received')
    vosfor: Optional[int] = Field(default=None, sa_column=Column(SmallInteger, nullable=True),
                                  description='Resource obtained by melting arcane')
    reputation: Optional[int] = Field(default=None, nullable=True,
                                      description='Required amount of reputation to purchase')


class ArcaneCreate(ArcaneBase):
    pass


# Arcane Location
class ArcaneLocationBase(SQLModel):
    name: str


class ArcaneLocation(ArcaneLocationBase, table=True):
    __tablename__ = 'arcane_locations'
    id: Optional[int] = Field(default=None,
                              sa_column=Column(Integer, primary_key=True, autoincrement=True, nullable=True))
    name: str = Field(sa_column=Column(String(63), nullable=False))


class ArcaneLocationCreate(ArcaneLocationBase):
    pass


# Mod
class ModBase(SQLModel):
    rarity: Optional[str]
    mod_max_rank: int


class Mod(ModBase, table=True):
    __tablename__ = 'mods'
    item_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False,
                               foreign_key='items.item_id')
    rarity: Optional[str] = Field(default=None, sa_column=Column(String(63), nullable=True))
    mod_max_rank: int = Field(sa_column=Column(SmallInteger, nullable=False))


class ModCreate(ModBase):
    pass


# Weapon
class WeaponBase(SQLModel):
    item_id: uuid.UUID
    set_root: bool
    main_root: Optional[bool]
    root_id: Optional[List[uuid.UUID]]
    quantity_for_set: Optional[int]
    mastery_level: Optional[int]
    ducats: Optional[int]


class Weapon(WeaponBase, table=True):
    __tablename__ = 'weapons'
    item_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False,
                               foreign_key='items.item_id')
    set_root: bool = Field(default=False, description='Is the item part of a set')
    main_root: bool = Field(default=None, nullable=True, description='Is the item a blueprint')
    root_id: Optional[List[uuid.UUID]] = Field(default=None, sa_column=Column(ARRAY(UUID), nullable=True),
                                               description='Items id in set')
    quantity_for_set: Optional[int] = Field(default=None, sa_column=Column(SmallInteger, nullable=True),
                                            description='How many parts is in the set')
    mastery_level: Optional[int] = Field(default=None, sa_column=Column(SmallInteger, nullable=True),
                                         description='Mastery requirenment')
    ducats: Optional[int] = Field(default=None, sa_column=Column(SmallInteger, nullable=True),
                                  description='Mastery requirenment')


class WeaponCreate(WeaponBase):
    pass


# Relics
class RelicBase(SQLModel):
    item_id: uuid.UUID
    drops: Optional[List[uuid.UUID]]


class Relic(RelicBase, table=True):
    __tablename__ = 'relics'
    item_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False,
                               foreign_key='items.item_id')
    drops: Optional[List[uuid.UUID]] = Field(default=None, sa_column=Column(ARRAY(UUID), nullable=True))


class RelicCreate(RelicBase):
    pass


# Sculptures
class SculptureBase(SQLModel):
    item_id: uuid.UUID
    amber_stars: int
    cyan_stars: int


class Sculpture(SculptureBase, table=True):
    __tablename__ = 'sculptures'
    item_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False,
                               foreign_key='items.item_id')
    amber_stars: int = Field(sa_column=Column(SmallInteger, nullable=False), description='Max amount of amber stars')
    cyan_stars: int = Field(sa_column=Column(SmallInteger, nullable=False), description='Max amount of cyan stars')


class SculptureCreate(SculptureBase):
    pass


# l18n
class L18nBase(SQLModel):
    item_id: uuid.UUID
    language: str
    item_name: str
    description: Optional[str]
    wiki_link: Optional[str]


class L18n(L18nBase, table=True):
    __tablename__ = 'l18n'
    id: int = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True, nullable=False))
    item_id: uuid.UUID = Field(default_factory=uuid.uuid4, nullable=False, foreign_key='items.item_id')
    language: str = Field(sa_column=Column(String(7), nullable=False), description='ISO 639-1')
    item_name: str = Field(default=None, sa_column=Column(String(255), nullable=True), description='Item name')
    description: str = Field(default=None, sa_column=Column(Text, nullable=True), description='Item description')
    wiki_link: str = Field(default=None, sa_column=Column(String(511), nullable=True),
                           description='Link to the item wikipedia page')


class L18nCreate(L18nBase):
    pass


# items_update
class ItemUpdateBase(SQLModel):
    item_id: uuid.UUID
    wfm_id: str
    url_name: str


class ItemUpdate(ItemUpdateBase, table=True):
    __tablename__ = 'items_update'
    item_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False,
                               foreign_key='items.item_id')
    wfm_id: str = Field(nullable=False, unique=True, foreign_key='items.wfm_id', description='Warframe market item id')
    url_name: str = Field(nullable=False, unique=True, foreign_key='items.url_name', description='Warframe market url')


class ItemUpdateCreate(ItemUpdateBase):
    pass


# orders
class OrderBase(SQLModel):
    order_id: str
    item_id: uuid.UUID
    url_name: str
    platinum: int
    quantity: int
    order_type: str
    rank: int
    platform: str = 'pc'
    creation_date: datetime
    last_update: datetime | None
    user_id: Optional[str]
    user_ingame_name: Optional[str]
    user_reputation: Optional[int]
    user_last_seen: datetime
    user_avatar: str


class Order(OrderBase, table=True):
    __tablename__ = 'orders'
    order_id: str = Field(sa_column=Column(String(63), primary_key=True, unique=True, nullable=False))
    item_id: uuid.UUID = Field(default_factory=uuid.uuid4, nullable=False, foreign_key='items.item_id')
    url_name: str = Field(sa_column=Column(String(63), nullable=False, unique=False), description='Warframe market url')
    platinum: int = Field(nullable=False)
    quantity: int = Field(nullable=False)
    order_type: str = Field(nullable=False)
    rank: int = Field(sa_column=Column(SmallInteger, nullable=True, unique=False))
    platform: str = Field(default='pc', sa_column=Column(String(7), nullable=False))
    creation_date: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    last_update: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    user_id: Optional[str] = Field(default=None, sa_column=Column(String(63), nullable=True))
    user_ingame_name: Optional[str] = Field(default=None, sa_column=Column(String(63), nullable=True))
    user_reputation: Optional[int] = Field(default=None, sa_column=Column(SmallInteger, nullable=True))
    user_last_seen: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    user_avatar: Optional[str] = Field(default=None, sa_column=Column(String(255), nullable=True))


class OrderCreate(OrderBase):
    pass


# roles
class RoleBase(SQLModel):
    name: str
    permission: int


class Role(RoleBase, table=True):
    __tablename__ = 'roles'
    id: int = Field(sa_column=Column(SmallInteger, primary_key=True, autoincrement=True))
    name: str = Field(sa_column=Column(String(31), nullable=False))
    permissions: int = Field(default=0, sa_column=Column(SmallInteger, nullable=False))


class RoleCreate(RoleBase):
    pass


# auth
class AuthBase(SQLModel):
    id: uuid.UUID
    email: str
    login: str
    hash_password: str
    registered_at: datetime
    role: int
    is_active: bool
    is_superuser: bool


class Auth(AuthBase, table=True):
    __tablename__ = 'auth'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False, )
    email: str = Field(unique=True, nullable=False)
    login: str = Field(sa_column=Column(String(31), nullable=False, unique=True))
    hash_password: str = Field(nullable=False)
    registered_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    role: int = Field(default=1, foreign_key='roles.id')
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)


class AuthCreate(AuthBase):
    pass


# types
class TypeBase(SQLModel):
    type: str


class Type(TypeBase, table=True):
    __tablename__ = 'types'
    id: int = Field(sa_column=Column(SmallInteger, primary_key=True, autoincrement=True))
    type: str = Field(sa_column=Column(String(31), nullable=False))


class TypeCreate(TypeBase):
    pass


'''
    types:
      - mystic
      - weapon
      - mod
      - relic
      - sculpture
'''


# tag_names
class TagNameBase(SQLModel):
    tag: str


class TagName(TagNameBase, table=True):
    __tablename__ = 'tag_names'
    id: int = Field(sa_column=Column(SmallInteger, primary_key=True, autoincrement=True))
    tag: str = Field(sa_column=Column(String(31), nullable=False))


class TagNameCreate(TagNameBase):
    pass


# tags
class TagBase(SQLModel):
    item_id: uuid.UUID
    tag_id: int


class Tag(TagBase, table=True):
    __tablename__ = 'tags'
    id: int = Field(sa_column=Column(SmallInteger, primary_key=True, autoincrement=True))
    item_id: uuid.UUID = Field(nullable=False, foreign_key='items.item_id')
    tag_id: int = Field(nullable=False, foreign_key='tag_names.id')


class TagCreate(TagBase):
    pass


# subtype_names
class SubtypeNameBase(SQLModel):
    tag: str


class SubtypeName(SubtypeNameBase, table=True):
    __tablename__ = 'subtype_names'
    id: int = Field(sa_column=Column(SmallInteger, primary_key=True, autoincrement=True))
    tag: str = Field(sa_column=Column(String(31), nullable=False))


class SubtypeNameCreate(SubtypeNameBase):
    pass


# subtypes
class SubtypeBase(SQLModel):
    item_id: uuid.UUID
    tag_id: int


class Subtype(SubtypeBase, table=True):
    __tablename__ = 'subtypes'
    id: int = Field(sa_column=Column(SmallInteger, primary_key=True, autoincrement=True))
    item_id: uuid.UUID = Field(nullable=False, foreign_key='items.item_id')
    tag_id: int = Field(nullable=False, foreign_key='subtype_names.id')


class SubtypeCreate(SubtypeBase):
    pass
