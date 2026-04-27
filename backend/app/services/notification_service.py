from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.services.socket_manager import socket_app

class NotificationService:
    @staticmethod
    async def create_notification(db: Session, user_id: str, title: str, message: str, type: str):
        # 1. Save to DB
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=type
        )
        db.add(notif)
        db.commit()
        db.refresh(notif)
        
        # 2. Emit via WebSocket
        from app.services.socket_manager import socket_manager
        delivered_ws = await socket_manager.notify_user(
            user_id, 
            {
                "id": notif.id,
                "title": notif.title,
                "message": notif.message,
                "type": notif.type,
                "created_at": str(notif.created_at)
            }
        )
        
        # 3. Mobile Native Push (Expo)
        from app.models.user import User
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.push_token:
            import httpx
            async with httpx.AsyncClient() as client:
                await client.post(
                    "https://exp.host/--/api/v2/push/send",
                    json={
                        "to": user.push_token,
                        "title": title,
                        "body": message,
                        "data": {"notification_id": notif.id},
                        "sound": "default"
                    }
                )
                print(f"EXPO PUSH: Sent to {user_id}")

        return notif

notification_service = NotificationService()
