from fastapi import FastAPI
from routers import news,users,favorite,history
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handlers import register_exception_handlers

app = FastAPI()
#注册异常处理器
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #允许的源，开发阶段允许所有源，生产阶段需要指定的源
    allow_credentials=True,#允许携带cookie
    allow_methods=["*"],#允许的请求方式
    allow_headers=["*"],#允许的请求头
)
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)