from fastapi import FastAPI, BackgroundTasks
from services.lnm import send_stk
from .routers import users, units, lnm, ussd
# create database tables
# ToDo : initialize database and run migrations with alembic instead
# models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/stk_push")
async def stkPush(background_tasks: BackgroundTasks, amount: int = 1):
    background_tasks.add_task(send_stk, amount)
    return {"Message": "Payment initiated"}

app.include_router(users.router)
app.include_router(units.router)
app.include_router(lnm.router)
app.include_router(ussd.router)
