from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
#数据库引擎 函数调用
DATABASE_URL="mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8"
db_engine=create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)
#创建异步会话工厂 函数调用
AsyncSessionLocal=async_sessionmaker(
    bind=db_engine,
    expire_on_commit=False,
    class_=AsyncSession
    )
#依赖性，在会话工厂里面获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()