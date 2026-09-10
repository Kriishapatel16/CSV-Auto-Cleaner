import sys
import os

# Force Python to look in the root folder for app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

app = app