from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_async_session
from models.models import menu, submenu, dish
from models.shema import Menu_Create, Menu

router = APIRouter(
    prefix="/menus",
    tags=["Menu"]
)
def get_menu(menu,submenus_count,dishes_count):
    return {
        "id":menu[0],
        "title": menu[1],
        "description": menu[2],
        "submenus_count":len(submenus_count),
        "dishes_count":dishes_count
    }
@router.get("/")
async def GET_all_menus(session: AsyncSession = Depends(get_async_session)):
    query = select(menu)
    result = await session.execute(query)
    await session.commit()
    res=[]
    for x in result.all():
        submenus_count = await session.execute(select(submenu).where(submenu.c.menu_id==x[0]))
        submenus_count = submenus_count.all()
        await session.commit()
        dc=0
        for y in submenus_count:
            print(y)
            dishes_count = await session.execute(select(dish).where(dish.c.submenu_id==y[0]))
            dishes_count = dishes_count.all()
            await session.commit()
            dc+=len(dishes_count)

        res.append(get_menu(x,submenus_count,dc))
    return res

@router.get("/{menu_id}",status_code=200,response_model=Menu)
async def GET_one_menus(menu_id:UUID, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(menu).where(menu.c.id==menu_id)
        result = await session.execute(query)
        result=result.all()
        submenus_count = await session.execute(select(submenu).where(submenu.c.menu_id == result[0][0]))
        await session.commit()
        submenus_count=submenus_count.all()

        dc=0
        for y in submenus_count:
            print(y)
            dishes_count = await session.execute(select(dish).where(dish.c.submenu_id==y[0]))
            dishes_count = dishes_count.all()
            await session.commit()
            dc+=len(dishes_count)

        return get_menu(result[0],submenus_count,dc)
    except:
        return HTTPException(status_code=200, detail={
            "detail": "menu not found"
            })

@router.post("/",status_code=201)
async def POST_new_menus(new_menu:Menu_Create, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(menu).values(**new_menu.dict())
    stmt = stmt.returning(menu.c.id, menu.c.title, menu.c.description)
    res = await  session.execute(stmt)
    await session.commit()
    return HTTPException(status_code=201, detail=get_menu(res.all()[0],[],0))

@router.delete("/{menu_id}")
async def DELETE_menu(menu_id:UUID,session: AsyncSession = Depends(get_async_session)):
    query = menu.delete().where(menu.c.id == menu_id)
    await session.execute(query)
    await session.commit()
    return HTTPException(status_code=200, detail={
    "status": True,
    "message": "The menu has been deleted"
})

@router.put("/{menu_id}",status_code=200)
async def UPDATE_menu(menu_id: UUID, menu_data: Menu_Create, session: AsyncSession = Depends(get_async_session)):
    try:
        query = menu.update().where(menu.c.id == menu_id).values(**menu_data.dict())
        await session.execute(query)
        await session.commit()
        query = select(menu).where(menu.c.id == menu_id)
        result = await session.execute(query)
        result = result.all()
        submenus_count = await session.execute(select(submenu).where(submenu.c.menu_id == result[0][0]))
        await session.commit()
        submenus_count = submenus_count.all()
        dishes_count = 0
        for y in submenus_count:
            dish_ = await session.execute(select(dish).where(dish.c.submenu_id == y[0]))
            await session.commit()
            dishes_count += len(dish_.all())
        return get_menu(result[0], submenus_count, dishes_count)
    except:
        return HTTPException(status_code=200,detail= {
    "detail": "menu not found"
})