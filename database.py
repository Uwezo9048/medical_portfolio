import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from config import Config

@dataclass
class Client:
    """Client/Contact submission model"""
    id: int = 0
    name: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    project_type: str = ""
    message: str = ""
    status: str = "new"
    created_at: str = ""
    read_by_admin: bool = False
    admin_notes: str = ""
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'project_type': self.project_type,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at,
            'read_by_admin': self.read_by_admin,
            'admin_notes': self.admin_notes
        }

@dataclass
class WebsiteContent:
    """Website content storage model"""
    section: str = ""
    content: str = ""
    updated_at: str = ""
    
    def to_dict(self):
        return {
            'section': self.section,
            'content': self.content,
            'updated_at': self.updated_at
        }

@dataclass 
class AdminUser:
    """Admin user model"""
    id: int = 0
    username: str = ""
    password_hash: str = ""
    created_at: str = ""
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at
        }

class DatabaseManager:
    """SQLite database manager"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or Config.DATABASE_PATH
        self.init_database()
    
    def get_connection(self):
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with required tables"""
        # [Keep all database initialization code from original]
        # ... (truncated for brevity, include all methods)