from pydantic import BaseModel


class IngestResult(BaseModel):
    doc_id: str
    file_name: str
    chunk_count: int


class DeleteResult(BaseModel):
    doc_id: str
    deleted: bool = True


class KnowledgeDoc(BaseModel):
    doc_id: str
    file_name: str
    chunk_count: int