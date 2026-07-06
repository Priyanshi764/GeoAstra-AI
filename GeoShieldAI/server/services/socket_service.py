"""
Socket.IO Service for GeoShield AI
Handles real-time updates and event broadcasts to the frontend
"""
import socketio
import os

# Initialize Socket.IO Server
sio = socketio.Server(cors_allowed_origins="*")

class SocketService:
    """Manages Socket.IO events and connections"""
    
    @staticmethod
    def init_app(app):
        """Wrap Flask app with Socket.IO WSGI middleware if needed"""
        try:
            # Create a WSGI App that wraps flask app with socket.io
            wsgi_app = socketio.WSGIApp(sio, app)
            return wsgi_app
        except Exception as e:
            print(f"[SOCKETIO] Error initializing: {str(e)}")
            return app
            
    @staticmethod
    def broadcast_event(event_name, data):
        """Broadcast event to all connected clients"""
        try:
            sio.emit(event_name, data)
            print(f"[SOCKETIO] Broadcasted event '{event_name}' successfully.")
        except Exception as e:
            # Fail silently in case socket is not fully initialized
            print(f"[SOCKETIO] Broadcast failed: {str(e)}")

# Define connection events
@sio.event
def connect(sid, environ):
    print(f"[SOCKETIO] Client connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"[SOCKETIO] Client disconnected: {sid}")
