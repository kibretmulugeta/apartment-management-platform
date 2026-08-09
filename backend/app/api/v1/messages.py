from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.message import Conversation, Message, Notification
from app.schemas.common import APIResponse
from app.api.dependencies import get_current_user, get_current_org_id
from app.models.user import User

router = APIRouter(prefix="/messages", tags=["Messages & Notifications"])

@router.get("/conversations", response_model=APIResponse[List[dict]])
def get_user_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    convs = db.query(Conversation).filter(
        (Conversation.tenant_id == current_user.id) | (Conversation.manager_id == current_user.id)
    ).all()
    res = []
    for c in convs:
        last_msg = db.query(Message).filter(Message.conversation_id == c.id).order_by(Message.created_at.desc()).first()
        other_user = c.manager if c.tenant_id == current_user.id else c.tenant
        res.append({
            "id": c.id,
            "title": c.title or f"Chat with {other_user.full_name}",
            "other_user": {
                "id": other_user.id,
                "name": other_user.full_name,
                "avatar": other_user.avatar_url
            },
            "last_message": last_msg.content if last_msg else "No messages yet",
            "last_message_at": last_msg.created_at if last_msg else c.created_at
        })
    return APIResponse(success=True, data=res)

@router.get("/conversations/{conversation_id}", response_model=APIResponse[List[dict]])
def get_messages(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv or (conv.tenant_id != current_user.id and conv.manager_id != current_user.id):
        raise HTTPException(status_code=403, detail="Forbidden")

    msgs = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()
    res = [{
        "id": m.id,
        "sender_id": m.sender_id,
        "sender_name": m.sender.full_name,
        "is_me": m.sender_id == current_user.id,
        "content": m.content,
        "created_at": m.created_at
    } for m in msgs]
    return APIResponse(success=True, data=res)

@router.post("/conversations/{conversation_id}/send", response_model=APIResponse[dict])
def send_message(
    conversation_id: str,
    content: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv or (conv.tenant_id != current_user.id and conv.manager_id != current_user.id):
        raise HTTPException(status_code=403, detail="Forbidden")

    msg = Message(
        conversation_id=conversation_id,
        sender_id=current_user.id,
        content=content
    )
    db.add(msg)
    db.commit()
    return APIResponse(success=True, message="Message sent", data={"id": msg.id, "content": msg.content})

@router.get("/notifications", response_model=APIResponse[List[dict]])
def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notifs = db.query(Notification).filter(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()).all()
    res = [{
        "id": n.id,
        "title": n.title,
        "message": n.message,
        "type": n.type,
        "is_read": n.is_read,
        "created_at": n.created_at
    } for n in notifs]
    return APIResponse(success=True, data=res)
