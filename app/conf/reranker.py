import os
from app.conf.app_config import root_project
import torch

MODEL_PATH = os.getenv(
    "MODEL_DIR",
    str(root_project / "docker" / "reranker" / "bge-reranker-base"),
)
DEVICE = os.getenv("MODEL_DEVICE", "cuda" if torch.cuda.is_available() else "cpu")
MAX_SEQ_LENGTH = 512