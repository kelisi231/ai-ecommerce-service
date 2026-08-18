import os
import torch
from sentence_transformers import SentenceTransformer
from app.conf.app_config import root_project

MODEL_PATH = os.getenv(
    "MODEL_DIR",
    str(root_project / "docker" / "embedding" / "bge-small-zh-v1.5"),
)
DEVICE = os.getenv("MODEL_DEVICE", "cuda" if torch.cuda.is_available() else "cpu")
MAX_SEQ_LENGTH = 512



