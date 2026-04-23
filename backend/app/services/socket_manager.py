import socketio
from typing import Dict, Any

# Create an Async Server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")

class SocketManager:
    def __init__(self):
        # Map user_id to sid (session ID)
        self.user_to_sid: Dict[str, str] = {}
        self.sid_to_user: Dict[str, str] = {}

    async def connect(self, sid, environ):
        # Extract user_id from auth headers if needed
        # For now, we'll wait for a 'register' event or extract from token
        print(f"Client connected: {sid}")

    async def disconnect(self, sid):
        user_id = self.sid_to_user.get(sid)
        if user_id:
            print(f"User {user_id} disconnected")
            del self.user_to_sid[user_id]
            del self.sid_to_user[sid]
        else:
            print(f"Unregistered client disconnected: {sid}")

    async def handle_register(self, sid, data: Dict[str, Any]):
        user_id = str(data.get("user_id"))
        if user_id:
            self.user_to_sid[user_id] = sid
            self.sid_to_user[sid] = user_id
            print(f"User {user_id} registered with sid {sid}")
            await sio.emit("registered", {"status": "success"}, to=sid)

    async def handle_message(self, sid, data: Dict[str, Any]):
        sender_id = self.sid_to_user.get(sid)
        target_id = str(data.get("target_id"))
        message_text = data.get("message")
        
        if sender_id and target_id and message_text:
            # Persistent Storage
            from app.core.database import SessionLocal
            from app.services.chat_service import save_message
            
            with SessionLocal() as db:
                save_message(db, int(sender_id), int(target_id), message_text)

            target_sid = self.user_to_sid.get(target_id)
            if target_sid:
                await sio.emit("message", {
                    "from": sender_id,
                    "message": message_text
                }, to=target_sid)
                print(f"Message from {sender_id} to {target_id} delivered & saved")
            else:
                print(f"Target user {target_id} offline, message saved to DB")

socket_manager = SocketManager()

# Event Handlers
@sio.event
async def connect(sid, environ):
    await socket_manager.connect(sid, environ)

@sio.event
async def disconnect(sid):
    await socket_manager.disconnect(sid)

@sio.on("register")
async def register(sid, data):
    await socket_manager.handle_register(sid, data)

@sio.on("message")
async def message(sid, data):
    await socket_manager.handle_message(sid, data)

# Wrap with ASGI app
socket_app = socketio.ASGIApp(sio)
