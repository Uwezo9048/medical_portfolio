import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from typing import Tuple, Optional, Dict

class AuthManager:
    """JWT authentication manager"""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key
        self.algorithm = "HS256"
    
    def create_token(self, admin_data: Dict) -> str:
        """Create JWT token"""
        payload = {
            'admin': admin_data,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Tuple[bool, Optional[Dict]]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return True, payload.get('admin')
        except jwt.ExpiredSignatureError:
            return False, "Token has expired"
        except jwt.InvalidTokenError:
            return False, "Invalid token"
    
    def get_auth_header(self) -> Optional[str]:
        """Get authorization header from request"""
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return None
    
    def login_required(self, f):
        """Decorator to require authentication for routes"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = self.get_auth_header()
            if not token:
                return jsonify({'error': 'Authentication required'}), 401
            
            success, admin_data = self.verify_token(token)
            if not success:
                return jsonify({'error': admin_data}), 401
            
            return f(*args, **kwargs)
        return decorated_function