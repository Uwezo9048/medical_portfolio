import sys
import os

# Get your username automatically
username = os.path.basename(os.path.expanduser('~'))
path = f'/home/{username}/medical_portfolio'

if path not in sys.path:
    sys.path.insert(0, path)

# Change to your project directory
os.chdir(path)

# Import the Flask app
from app import app

# PythonAnywhere requires the variable to be called 'application'
application = app