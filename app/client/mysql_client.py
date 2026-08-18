from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from app.conf.app_config import app_config, MySQLConfig

class MySQLClient:
    def __init__(self, db_config: MySQLConfig):
        self.db_config = db_config
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker[AsyncSession] | None = None

    def _get_url(self):
        return f"mysql+asyncmy://{self.db_config.user}:{self.db_config.password}@{self.db_config.host}:{self.db_config.port}/{self.db_config.database}?charset=utf8mb4"

    def init(self):
        self.engine = create_async_engine(
            self._get_url(),
            pool_size=10,
            pool_pre_ping=True
        )

        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=True
        )

    async def close(self):
        await self.engine.dispose()


mysql_client = MySQLClient(app_config.mysql)
