from fastapi import FastAPI
from router.router import router as router_operation
# from db.db import Base, engine

app = FastAPI(
    title="Task #1"
)
# @app.on_event("startup")
# async def startup():
#     Base.metadata.create_all(bind=engine)
#
# @app.on_event("shutdown")
# async def shutdown():
#     pass

app.include_router(router_operation)