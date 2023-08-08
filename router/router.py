from fastapi import APIRouter, Depends

from router.menu_router import router as menu_router
from router.submenu_router import router as submenu_router
from router.dish_router import router as dish_router

router = APIRouter(
    prefix="/api/v1",
    tags=["All routers"]
)
router.include_router(menu_router)
router.include_router(submenu_router)
router.include_router(dish_router)