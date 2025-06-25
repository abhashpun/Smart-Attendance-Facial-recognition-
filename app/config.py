import os

# Database configuration
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'attendance_db')
DB_USER = os.environ.get('DB_USER', 'attendance_user')
DB_PASS = os.environ.get('DB_PASS', 'abhash')

# Constants
FACE_RECOGNITION_THRESHOLD = 0.6
ATTENDANCE_COOLDOWN_SECONDS = 300

# CORS
ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]
