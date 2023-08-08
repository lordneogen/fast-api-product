from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_async_session
from models.models import menu, submenu, dish
from models.shema import Menu_Create, Menu, SubMenu_Create, Dish_Create

router = APIRouter(
    prefix="/menus",
    tags=["Dish"]
)
def get_submenu(submenu):
    return {
        "id":submenu[0],
        "title": submenu[1],
        "description": submenu[2],
        "price":submenu[3]
    }

@router.get("/{menu_id}/submenus/{submenu_id}/dishes")
async def GET_all_dishes(menu_id:UUID,submenu_id:UUID,session: AsyncSession = Depends(get_async_session)):
    query = select(dish).where(dish.c.submenu_id==submenu_id)
    result = await session.execute(query)
    await session.commit()
    res=[]
    for x in result.all():
        res.append(get_submenu(x))
    return res

@router.post("/{menu_id}/submenus/{submenu_id}/dishes",status_code=201)
async def POST_new_dish(menu_id:UUID, submenu_id:UUID, new_submenu:Dish_Create, session: AsyncSession = Depends(get_async_session)):

    stmt = insert(dish).values({
        "title":new_submenu.dict()['title'],
        "description":new_submenu.dict()['description'],
        "price": new_submenu.dict()['price'],
        "submenu_id":submenu_id
    })
    stmt= stmt.returning(dish.c.id,dish.c.title,dish.c.description,dish.c.price,dish.c.submenu_id)
    res =await  session.execute(stmt)
    await session.commit()
    return HTTPException(status_code=201, detail=get_submenu(res.all()[0]))

@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def DELETE_submenu(submenu_id:UUID,menu_id:UUID,dish_id:UUID,session: AsyncSession = Depends(get_async_session)):
    query = dish.delete().where(dish.c.id == dish_id , dish.c.dubmenu_id==submenu_id )
    await session.execute(query)
    await session.commit()
    return HTTPException(status_code=200, detail={
    "status": True,
    "message": "The dish has been deleted"
})