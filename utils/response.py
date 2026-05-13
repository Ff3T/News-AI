from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse


def success_response(message:str="success",data=None):
    content={
        "code":200,
        "message":message,
        "data":data
    }
    return JSONResponse(status_code=200,content=jsonable_encoder(content))
