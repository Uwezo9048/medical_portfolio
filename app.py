#!/usr/bin/env python3
"""
Medical Portfolio System - Single file for PythonAnywhere
"""

import os
import sys
import json
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps

# Third-party imports
try:
    from flask import Flask, request, jsonify, send_from_directory, render_template_string
    from flask_cors import CORS
    from werkzeug.security import generate_password_hash, check_password_hash
    from werkzeug.utils import secure_filename
    import jwt
except ImportError as e:
    print("Missing dependencies. Please install:")
    print("pip install flask flask-cors werkzeug pyjwt")
    sys.exit(1)

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['DATABASE_PATH'] = os.path.join(BASE_DIR, 'medical_portfolio.db')
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Create directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ==================== SIMPLE DATABASE SETUP ====================
def init_db():
    """Initialize the database"""
    conn = sqlite3.connect(app.config['DATABASE_PATH'])
    cursor = conn.cursor()
    
    # Create clients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            project_type TEXT,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'new',
            read_by_admin BOOLEAN DEFAULT 0,
            admin_notes TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create admin user
    cursor.execute('SELECT COUNT(*) FROM sqlite_master WHERE type="table" AND name="admin_users"')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            CREATE TABLE admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        # Add default admin
        password_hash = generate_password_hash("admin9048")
        cursor.execute('INSERT INTO admin_users (username, password_hash) VALUES (?, ?)', 
                      ('admin', password_hash))
    
    conn.commit()
    conn.close()

# ==================== SIMPLE ROUTES ====================
@app.route('/')
def index():
    """Main website"""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Medical Portfolio | Dr. Foscah Faith</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }
            .status {
                background: #27ae60;
                color: white;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
                margin: 20px 0;
            }
            .links {
                margin-top: 30px;
            }
            .links a {
                display: inline-block;
                margin: 10px;
                padding: 10px 20px;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
            .links a:hover {
                background: #2980b9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Medical Portfolio System</h1>
            <div class="status">
                ✅ System is running successfully!
            </div>
            <p>Welcome to the Medical Portfolio System for Dr. Foscah Faith.</p>
            <p>This is a health tech communication platform that helps translate complex medical concepts into clear, effective content.</p>
            
            <div class="links">
                <a href="/admin-portal">Go to Admin Portal</a>
                <a href="/api/health">Check API Health</a>
                <a href="/test-form">Test Contact Form</a>
            </div>
            
            <h2>System Information:</h2>
            <ul>
                <li>Database: {db_status}</li>
                <li>Upload Folder: {upload_status}</li>
                <li>PythonAnywhere: Active</li>
            </ul>
        </div>
    </body>
    </html>
    '''
    
    # Check if database exists
    db_status = "✅ Ready" if os.path.exists(app.config['DATABASE_PATH']) else "⚠️ Not found"
    upload_status = "✅ Ready" if os.path.exists(app.config['UPLOAD_FOLDER']) else "⚠️ Not found"
    
    return html.format(db_status=db_status, upload_status=upload_status)

@app.route('/admin-portal')
def admin_portal():
    """Simple admin portal"""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Portal</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 20px;
                background: #f0f0f0;
            }
            .admin-container {
                max-width: 400px;
                margin: 50px auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h2 {
                color: #2c3e50;
                text-align: center;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #555;
            }
            input {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-sizing: border-box;
            }
            button {
                width: 100%;
                padding: 12px;
                background: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background: #2980b9;
            }
            .back-link {
                text-align: center;
                margin-top: 20px;
            }
            .back-link a {
                color: #3498db;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="admin-container">
            <h2>Admin Portal Login</h2>
            <form id="loginForm">
                <div class="form-group">
                    <label>Username:</label>
                    <input type="text" id="username" value="admin" required>
                </div>
                <div class="form-group">
                    <label>Password:</label>
                    <input type="password" id="password" value="admin9048" required>
                </div>
                <button type="button" onclick="login()">Login</button>
            </form>
            <div class="back-link">
                <a href="/">← Back to Main Site</a>
            </div>
        </div>
        
        <script>
            async function login() {
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                
                try {
                    const response = await fetch('/api/admin/login', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({username, password})
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        alert('Login successful! Token: ' + data.access_token.substring(0, 20) + '...');
                    } else {
                        alert('Error: ' + data.error);
                    }
                } catch (error) {
                    alert('Login failed: ' + error);
                }
            }
        </script>
    </body>
    </html>
    '''
    return html

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Medical Portfolio API',
        'database': os.path.exists(app.config['DATABASE_PATH']),
        'python_version': sys.version,
        'platform': sys.platform
    })

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Simple admin login"""
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    if username == 'admin' and password == 'admin9048':
        # Create a simple token
        token = secrets.token_hex(32)
        return jsonify({
            'access_token': token,
            'admin': {'username': 'admin'},
            'message': 'Login successful'
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/test-form')
def test_form():
    """Test contact form"""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Contact Form</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            form { max-width: 500px; margin: 0 auto; }
            input, textarea { width: 100%; padding: 10px; margin: 10px 0; }
            button { background: #27ae60; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        </style>
    </head>
    <body>
        <h2>Test Contact Form</h2>
        <form id="contactForm">
            <input type="text" name="name" placeholder="Name" required><br>
            <input type="email" name="email" placeholder="Email" required><br>
            <textarea name="message" placeholder="Message" rows="5" required></textarea><br>
            <button type="button" onclick="submitForm()">Send Message</button>
        </form>
        <div id="result" style="margin-top: 20px;"></div>
        
        <script>
            async function submitForm() {
                const form = document.getElementById('contactForm');
                const data = {
                    name: form.name.value,
                    email: form.email.value,
                    message: form.message.value
                };
                
                try {
                    const response = await fetch('/api/clients', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    document.getElementById('result').innerHTML = 
                        response.ok ? 
                        '<span style="color: green;">✓ ' + result.message + '</span>' :
                        '<span style="color: red;">✗ Error: ' + result.error + '</span>';
                } catch (error) {
                    document.getElementById('result').innerHTML = 
                        '<span style="color: red;">✗ Network error: ' + error + '</span>';
                }
            }
        </script>
    </body>
    </html>
    '''
    return html

@app.route('/api/clients', methods=['POST'])
def create_client():
    """Create a new client submission"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Simple validation
    if not data.get('name') or not data.get('email') or not data.get('message'):
        return jsonify({'error': 'Name, email, and message are required'}), 400
    
    # Save to database
    conn = sqlite3.connect(app.config['DATABASE_PATH'])
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO clients (name, email, message)
        VALUES (?, ?, ?)
    ''', (data['name'], data['email'], data['message']))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'message': 'Thank you for your message! We will contact you soon.',
        'client': {
            'name': data['name'],
            'email': data['email']
        }
    }), 201

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

# Initialize database on startup
init_db()

if __name__ == '__main__':
    print("Starting Medical Portfolio System...")
    print(f"Database: {app.config['DATABASE_PATH']}")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"Visit: http://localhost:5000")
    app.run(debug=True)