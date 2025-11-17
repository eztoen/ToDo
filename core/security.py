from jose import JWTError, jwt
from typing import Optional
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from pydantic_settings import BaseSettings, SettingsConfigDict

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error, scheme_name="JWT")

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        credentials = await super().__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=403, 
                    detail="Invalid authentication scheme."
                )
            return credentials.credentials
        return None

oauth2_scheme = JWTBearer()

class Security(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    
    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expire_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expire_delta or timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({'exp': expire})
        return jwt.encode(
            to_encode, 
            key=self.SECRET_KEY, 
            algorithm=self.ALGORITHM
        )
        
    def create_refresh_token(self, data: dict, expire_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expire_delta or timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({'exp': expire})
        return jwt.encode(
            to_encode, 
            key=self.SECRET_KEY, 
            algorithm=self.ALGORITHM
        )
        
    async def get_user_id(self, token: str = Depends(oauth2_scheme)) -> int:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not valide credentials',
        )
        try:
            payload = jwt.decode(
                token, 
                key=self.SECRET_KEY, 
                algorithms=[self.ALGORITHM]
            )
            user_id: int = payload.get('sub')
            
            if user_id is None:
                raise credentials_exception
            
            return int(user_id)
        
        except JWTError:
            raise credentials_exception
        
    model_config = SettingsConfigDict(env_file='core/.env')
    
security = Security()