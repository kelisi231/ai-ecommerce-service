from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from omegaconf import OmegaConf


@dataclass
class MySQLConfig:
    host: str
    port: int
    user: str
    password: str
    database: str



@dataclass
class ESConfig:
    hosts: list[str]
    index_name: str


@dataclass
class QdrantConfig:
    host: str
    port: int
    embedding_size: int
    collection_name: str


@dataclass
class EmbeddingConfig:
    model: str
    url: str


@dataclass
class RerankerConfig:
    model: str
    url: str


@dataclass
class LogConfig:
    console_level: str
    file_level: str
    retention_days: int


@dataclass
class AppConfig:
    mysql: MySQLConfig
    es: ESConfig
    qdrant: QdrantConfig
    embedding: EmbeddingConfig
    reranker: RerankerConfig
    log: LogConfig


root_project = Path(__file__).parents[2]

load_dotenv(root_project / ".env")

context = OmegaConf.load(root_project / "conf" / "app_config.yaml")

schemas = OmegaConf.structured(AppConfig)

app_config: AppConfig = OmegaConf.to_object(OmegaConf.merge(schemas, context))

if __name__ == "__main__":
    print(app_config.mysql.user)
