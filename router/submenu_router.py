from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_async_session
from models.models import menu, submenu, dish
from models.shema import Menu_Create, Menu, SubMenu_Create

router = APIRouter(
    prefix="/menus",
    tags=["Submenu"]
)
def get_submenu(submenu, dishes_count):
    return {
        "id":submenu[0],
        "title": submenu[1],
        "description": submenu[2],
        "dishes_count":dishes_count
    }
@router.get("/{menu_id}/submenus")
async def GET_all_submenus(menu_id:UUID,session: AsyncSession = Depends(get_async_session)):
    query = select(submenu).where(submenu.c.menu_id==menu_id)
    result = await session.execute(query)
    await session.commit()
    res=[]
    for x in result.all():
        dish_ = await session.execute(select(dish).where(dish.c.submenu_id == x[0]))
        res.append(get_submenu(x,len(dish_.all())))
    return res

@router.post("/{menu_id}/submenus",status_code=201)
async def POST_new_submenus(menu_id:str, new_submenu:SubMenu_Create, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(submenu).values({
        "title":new_submenu.dict()['title'],
        "description":new_submenu.dict()['description'],
        "menu_id":menu_id
    })

    stmt= stmt.returning(submenu.c.id,submenu.c.title,submenu.c.description,submenu.c.menu_id)
    res =await  session.execute(stmt)
    await session.commit()
    return HTTPException(status_code=201, detail=get_submenu(res.all()[0],0))

@router.get("/{menu_id}/submenus/{submenu_id}")
async def GET_one_submenus(submenu_id:UUID,menu_id:UUID,session: AsyncSession = Depends(get_async_session)):
    query = select(submenu).where(submenu.c.menu_id==menu_id , submenu.c.id==submenu_id)
    result = await session.execute(query)
    await session.commit()
    res=[]
    for x in result.all():
        dish_ = await session.execute(select(dish).where(dish.c.submenu_id == x[0]))
        res.append(get_submenu(x,len(dish_.all())))
    if len(res)>0:
        return res[0]
    else:
        return {
            "detail": "submenu not found"
        }

@router.delete("/{menu_id}/submenus/{submenu_id}")
async def DELETE_submenu(submenu_id:UUID,menu_id:UUID,session: AsyncSession = Depends(get_async_session)):
    query = submenu.delete().where(submenu.c.id == submenu_id , submenu.c.menu_id==menu_id )
    await session.execute(query)
    await session.commit()
    return HTTPException(status_code=200, detail={
    "status": True,
    "message": "The menu has been deleted"
})

@router.put("/{menu_id}/submenus/{submenu_id}",status_code=200)
async def UPDATE_submenu(submenu_id:UUID,menu_id:UUID, menu_data: SubMenu_Create, session: AsyncSession = Depends(get_async_session)):
    try:
        query = submenu.update().where(submenu.c.id == submenu_id , submenu.c.menu_id==menu_id ).values(**menu_data.dict())
        await session.execute(query)
        await session.commit()
        query = select(submenu).where(submenu.c.id == submenu_id , submenu.c.menu_id==menu_id)
        result = await session.execute(query)
        await session.commit()
        res = []
        for x in result.all():
            dish_ = await session.execute(select(dish).where(dish.c.submenu_id == x[0]))
            res.append(get_submenu(x, len(dish_.all())))
        if len(res) > 0:
            return res[0]
        else:
            return {
                "detail": "submenu not found"
            }
    except:
        return HTTPException(status_code=200,detail= {
    "detail": "menu not found"
})