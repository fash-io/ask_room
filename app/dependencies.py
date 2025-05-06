from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
import httpx
import os
from app.models import User
from app.crud import user as crud_user
from app.database import SessionLocal


# Get project details from environment variables
SUPABASE_PROJECT_ID = os.getenv("SUPABASE_PROJECT_ID")
JWKS_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co/auth/v1/keys"
AUDIENCE = os.getenv("SUPABASE_JWT_AUDIENCE", "authenticated")
ISSUER = f"https://{SUPABASE_PROJECT_ID}.supabase.co/auth/v1"

_cached_keys = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fetch the JWKS (JSON Web Key Set) from Supabase
async def get_jwks():
    global _cached_keys
    if not _cached_keys:
        async with httpx.AsyncClient() as client:
            response = await client.get(JWKS_URL)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Could not fetch JWKS")
            _cached_keys = response.json()
    return _cached_keys

# Get the current user from the token
async def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]
    jwks = await get_jwks()

    try:
        unverified_header = jwt.get_unverified_header(token)
        key = next((k for k in jwks["keys"] if k["kid"] == unverified_header["kid"]), None)
        if not key:
            raise HTTPException(status_code=401, detail="Invalid token key")

        public_key = jwt.construct_rsa_public_key(key)
        payload = jwt.decode(token, public_key, algorithms=[key["alg"]], audience=AUDIENCE, issuer=ISSUER)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
