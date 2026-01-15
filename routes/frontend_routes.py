from flask import render_template_string, send_from_directory
from templates import HTML_TEMPLATE
import os

def register_frontend_routes(app):
    """Register frontend routes"""
    
    @app.route('/')
    @app.route('/<path:path>')
    def serve_frontend(path=''):
        """Serve the HTML frontend"""
        return render_template_string(HTML_TEMPLATE)
    
    @app.route('/static/<path:filename>')
    def serve_static(filename):
        return send_from_directory('static', filename)