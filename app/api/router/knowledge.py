from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.dependencies import get_knowledge_service
from app.api.model.knowledge import DeleteResult, IngestResult, KnowledgeDoc
from app.service.knowledge import KnowledgeIngestionService

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.post("/upload", response_model=list[IngestResult])
async def upload(
        files: list[UploadFile] = File(...),
        service: KnowledgeIngestionService = Depends(
            get_knowledge_service)
):
    results = []
    for file in files:
        if not file.filename:
            raise HTTPException(status_code=400, detail="文件名缺失")

        content = await file.read()
        try:
            result = await service.ingest(file.filename, content)

        finally:
            await file.close()

        results.append(result)
    return results


@router.get("/list", response_model=list[KnowledgeDoc])
async def list_docs(
        service: KnowledgeIngestionService = Depends(get_knowledge_service)
):
    return await service.list_docs()


@router.delete("/delete", response_model=DeleteResult)
async def delete(
        doc_id: str,
        service: KnowledgeIngestionService = Depends(get_knowledge_service)
):
     result =  await service.delete(doc_id)
     return result