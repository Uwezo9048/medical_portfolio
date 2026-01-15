from flask import render_template_string
from templates import ADMIN_PORTAL_TEMPLATE, ADMIN_LOGIN_TEMPLATE

def register_admin_routes(app):
    """Register admin portal routes"""
    
    @app.route('/admin-portal', methods=['GET'])
    def admin_portal():
        """Dedicated admin portal page"""
        return render_template_string(ADMIN_PORTAL_TEMPLATE)
    
    @app.route('/admin-login', methods=['GET'])
    def admin_login_page():
        """Simple admin login page that redirects to admin portal"""
        return render_template_string(ADMIN_LOGIN_TEMPLATE)