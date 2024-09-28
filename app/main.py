from fastapi import FastAPI
from .config import settings
from .db.mongo import connect_to_mongo, close_mongo_connection, get_mongo_client
from .routes.user_routes import user_router

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

app.include_router(user_router, prefix="/users")

# Endpoint de prueba
@app.get("/")
async def root():

    return {"message": "Bienvenido a la API de gestión de usuarios con FastAPI y MongoDB"}
