from uuid import UUID

from pydantic import BaseModel

# Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
# Column("title", String),
# Column("description", String)

class Menu_Create(BaseModel):
    title:str
    description:str

class SubMenu_Create(BaseModel):
    title:str
    description:str

class Dish_Create(BaseModel):
    title:str
    description:str
    price:str

class Menu(BaseModel):
    id:UUID
    title:str
    description:str
    submenus_count:int
    dishes_count:int
