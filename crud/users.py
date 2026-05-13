from datetime import datetime,timedelta

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from models.users import User,UserToken
from schemas.users import UserRequest, UserUpdateResponse,UserChangePasswordRequest
from utils import security
import uuid
#查询用户
async def get_user_by_username(db:AsyncSession,username:str):
    query=select(User).where(User.username==username)
    result=await db.execute(query)
    return result.scalar_one_or_none()
#注册用户
async def create_user(db:AsyncSession,user_data:UserRequest):
    hashed_password=security.get_password_hash(user_data.password)
    user=User(username=user_data.username,password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
#检查是否有用户令牌，没有就创建
async def create_token(db:AsyncSession,user_id:int):
    token=str(uuid.uuid4())
    expires_at=datetime.now()+timedelta(days=7)
    query=select(UserToken).where(UserToken.user_id==user_id)
    result=await db.execute(query)
    user_token=result.scalar_one_or_none()
    if user_token:
        user_token.token=token
        user_token.expires_at=expires_at
    else:
        user_token=UserToken(user_id=user_id,token=token,expires_at=expires_at)
        db.add(user_token)
        await db.commit()
    return token
#查看用户是否存在
async def authenticate_user(db:AsyncSession,user_data: UserRequest):
    user=await get_user_by_username(db,user_data.username)
    if not user:
        return None
    if not security.verify_password(user_data.password,user.password):
        return None
    return user
#得到用户令牌
async def get_user_by_token(db:AsyncSession,token:str):
    query=select(UserToken).where(UserToken.token==token)
    result=await db.execute(query)
    db_token=result.scalar_one_or_none()
    if not db_token or db_token.expires_at < datetime.now():
        return None
    query=select(User).where(User.id == db_token.user_id)
    result=await db.execute(query)
    return result.scalar_one_or_none()

#更新用户信息
async def update_user(db:AsyncSession,user_data: UserUpdateResponse,username:str):
    query=update(User).where(User.username==username).values(
        **user_data.model_dump(exclude_unset=True,exclude_none=True)
    )
    result= await db.execute(query)
    await db.commit()
    if result.rowcount==0:
        raise HTTPException(status_code=404,detail="用户不存在")
    updated_user=await get_user_by_username(db,username,)
    return updated_user

#更改密码
async def change_password(db:AsyncSession,user:User,user_data:UserChangePasswordRequest):
    if not security.verify_password(user_data.old_password,user.password):
        return False
    hashed_new_password=security.get_password_hash(user_data.new_password)
    user.password=hashed_new_password
    await db.commit()
    await db.refresh(user)
    return True






