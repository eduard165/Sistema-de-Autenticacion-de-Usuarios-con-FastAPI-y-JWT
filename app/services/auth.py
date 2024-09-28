from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from ..models.user import TokenData
from ..db.mongo import get_mongo_client
from ..config import settings
from ..utils.hashing import verify_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(login: str, password: str):
    mongo_client = get_mongo_client()
    user = await mongo_client.user_database.users.find_one({"email": login})
    if not user:
        user = await mongo_client.user_database.users.find_one({"username": login})
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="No se pueden validar las credenciales")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    
    mongo_client = get_mongo_client()
    print (f"{mongo_client}")
    # Asegúrate de que mongo_client sea la instancia correcta
    user = await mongo_client.user_database.users.find_one({"username": token_data.username})
    if user is None:
        raise credentials_exception
    return user
