from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserRequest, UserInfoResponse, UserAuthResponse, UserUpdateResponse,UserChangePasswordRequest
from config.db_conf import get_db
from crud import users
from starlette import status
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["users"])
@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession=Depends(get_db)):#用户信息，db
    existing=await users.get_user_by_username(db,user_data.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户已存在")
    user=await users.create_user(db,user_data)
    token=await users.create_token(db,user.id)
    response_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功",data=response_data)

@router.post("/login")
async def login(user_data: UserRequest, db:AsyncSession=Depends(get_db)):
    user=await users.authenticate_user(db,user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户或密码错误")
    token = await users.create_token(db, user.id)
    response_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功",data=response_data)

@router.get("/info")
async def get_user_info(user=Depends(get_current_user)):
    return success_response(message="获取用户信息成功",data=UserInfoResponse.model_validate(user))

@router.put("/update")
async def update_user_info(user_data: UserUpdateResponse,user=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    updated_user=await users.update_user(db,user_data,user.username,)
    return success_response(message="用户修改成功",data=UserInfoResponse.model_validate(updated_user))

#修改密码
@router.put("/password")
async def update_password(user_data:UserChangePasswordRequest,user=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    res_change=await users.change_password(db,user,user_data)
    if not res_change:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="密码错误")
    return success_response(message="密码修改成功")

