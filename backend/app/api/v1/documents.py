from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.storage import storage_service
from app.models.document import Document
from app.schemas.common import APIResponse
from app.api.dependencies import get_current_user, get_current_org_id
from app.models.user import User

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.get("/", response_model=APIResponse[List[dict]])
def list_documents(
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    docs = db.query(Document).filter(Document.organization_id == org_id).all()
    res = []
    for d in docs:
        res.append({
            "id": d.id,
            "name": d.name,
            "category": d.category,
            "mime_type": d.mime_type,
            "download_url": storage_service.generate_signed_url(d.file_key),
            "created_at": d.created_at
        })
    return APIResponse(success=True, data=res)

@router.post("/upload", response_model=APIResponse[dict])
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form("GENERAL"),
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    content = await file.read()
    file_key = storage_service.save_file(content, file.filename, subfolder="documents")

    doc = Document(
        organization_id=org_id,
        uploader_id=current_user.id,
        name=file.filename,
        file_key=file_key,
        file_size_bytes=len(content),
        mime_type=file.content_type or "application/pdf",
        category=category
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return APIResponse(
        success=True,
        message="Document uploaded securely",
        data={
            "id": doc.id,
            "name": doc.name,
            "signed_url": storage_service.generate_signed_url(file_key)
        }
    )
