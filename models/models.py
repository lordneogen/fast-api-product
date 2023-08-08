import uuid

import sqlalchemy
from sqlalchemy import MetaData,Integer,String,TIME,Table,Column,UUID
from sqlalchemy.orm import relationship

meta = MetaData()

menu=Table(
    "menu",
    meta,
    Column("id",UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title",String),
    Column("description",String),
)
submenu=Table(
    "submenu",
    meta,
    Column("id",UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title",String),
    Column("description",String),
    Column("menu_id", sqlalchemy.ForeignKey("menu.id")),


)
dish=Table(
    "dish",
    meta,
    Column("id",UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title",String),
    Column("description",String),
    Column("price",String),
    Column("submenu_id", sqlalchemy.ForeignKey("submenu.id"))
)