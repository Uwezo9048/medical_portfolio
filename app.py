#!/usr/bin/env python3
"""
Medical Portfolio System with Admin Portal URL
Enhanced with dedicated admin portal at /admin-portal
"""

import os
from flask import Flask
from flask_cors import CORS
from config import Config

# Import route modules
from routes.api_routes import register_api_routes
from routes.admin_routes import register_admin_routes
from routes.frontend_routes import register_frontend_routes

# Import managers
from database import DatabaseManager
from auth import AuthManager

class MedicalPortfolioApp:
    """Main Flask application"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        
        # Enable CORS
        CORS(self.app)
        
        # Initialize managers
        self.db = DatabaseManager()
        self.auth = AuthManager(self.app.config['SECRET_KEY'])
        
        # Create static directory for uploaded files
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        # Register routes
        self.register_routes()
    
    def register_routes(self):
        """Register all application routes"""
        register_api_routes(self.app)
        register_admin_routes(self.app)
        register_frontend_routes(self.app)
    
    def get_app(self):
        """Get the Flask app instance"""
        return self.app

# Create application instance
medical_app = MedicalPortfolioApp()
app = medical_app.get_app()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("MEDICAL PORTFOLIO SYSTEM - WITH ADMIN PORTAL")
    print("="*60)
    print("\nStarting server...")
    print(f"• Website URL: http://localhost:5000")
    print(f"• Admin Portal: http://localhost:5000/admin-portal")
    print(f"• Admin Login: http://localhost:5000/admin-login")
    print(f"• API Base URL: http://localhost:5000/api")
    print(f"• Health Check: http://localhost:5000/api/health")
    print("\nADMIN ACCESS:")
    print("• Integrated Admin: Click on the doctor's name in top-left corner")
    print("• Dedicated Portal: Use /admin-portal URL")
    print("• Username: admin")
    print("• Password: admin9048")
    print("\nNEW FEATURE: Dedicated admin portal at /admin-portal!")
    print("\n" + "="*60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)