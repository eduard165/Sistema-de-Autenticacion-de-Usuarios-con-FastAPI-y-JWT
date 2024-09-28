from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..models.user import UserCreate, Token
from ..services.auth import  authenticate_user, create_access_token, get_current_user
from ..db.mongo import get_mongo_client
from ..utils.userSerialize import serialize_user
from ..utils.hashing import get_password_hash


user_router = APIRouter()

@user_router.post("/register/")
async def register_user(user: UserCreate):
    # Llamamos a get_mongo_client() aquí dentro
    mongo_client = get_mongo_client()  
    print(f"User: {mongo_client}")
    
    # Accedemos a la base de datos y la colección
    existing_user = await mongo_client.user_database.users.find_one({"email": user.email})
    
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    hashed_password = get_password_hash(user.password)
    user_data = {"username": user.username, "email": user.email, "hashed_password": hashed_password}
    
    await mongo_client.user_database.users.insert_one(user_data)
    
    return {"msg": "Usuario registrado exitosamente"}

@user_router.post("/token/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Nombre de usuario o contraseña incorrectos")

    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.get("/me/")
async def read_current_user(current_user = Depends(get_current_user)):
    return serialize_user(current_user)
