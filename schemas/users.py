from pydantic import BaseModel,Field,ConfigDict
from typing import Optional

class UserRequest(BaseModel):
    username: str
    password: str

class UserInfoBase(BaseModel):
    nickname:Optional[str]=Field(None,max_length=50,description="昵称")
    avatar:Optional[str]=Field(None,max_length=255,description="头像URL")
    gender:Optional[str]=Field(None,max_length=10,description="性别")
    bio:Optional[str]=Field(None,max_length=500,description="个人简介")

class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    model_config=ConfigDict(
        from_attributes=True
    )

class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse=Field(...,alias="userInfo")
    model_config=ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class UserUpdateResponse(UserInfoBase):
    phone:str=Field(None,description="手机号")

class UserChangePasswordRequest(BaseModel):
    old_password:str=Field(...,alias="oldPassword",description="旧密码")
    new_password:str=Field(...,min_length=6,alias="newPassword",description="新密码")

    class Config:
        populate_by_name = True