from fastapi import APIRouter, Depends, Body, HTTPException
from backend.app.auth.auth_bearer import JWTBearer
from backend.app.auth.auth_handler import signJWT

from backend.app import schemas
import backend.app.core.access as helper

router = APIRouter()


@router.post("/signup/")
async def create_user(user: schemas.UserSchema = Body(...)):
    token = {}
    if helper.add_user(user):
        token = signJWT(user.email)
    else:
        raise HTTPException(status_code=409, detail="User already registered !")
    return token


@router.post("/login/")
async def user_login(user: schemas.UserLoginSchema = Body(...)):
    token = {}
    if helper.check_user(user):
        token = signJWT(user.email)
    else:
        raise HTTPException(status_code=404, detail="User not found !")
    return token