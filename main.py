from fastapi import FastAPI
from routers import teachers, cars

app = FastAPI(title= "API CON VARIOS ROUTER")

app.include_router(teachers.router)
app.include_router(cars.router)