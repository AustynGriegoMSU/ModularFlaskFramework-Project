"""
Authentication module for Project L
Handles user registration, login, logout, and session management
"""

from flask import session, request, redirect, url_for, flash
import bcrypt
from functools import wraps
import re

class Auth:
    def __init__(self, db_manager=None):
        self.db = db_manager
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        return True, "Password is valid"
    
    def hash_password(self, password):
        """Hash password using bcrypt"""
        # Convert password to bytes and generate salt
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def check_password(self, password_hash, password):
        """Verify password against bcrypt hash"""
        password_bytes = password.encode('utf-8')
        hash_bytes = password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    
    def register_user(self, username, email, password):
        """Register a new user"""
        try:
            # Validate input
            if not self.validate_email(email):
                return False, "Invalid email format"
            
            is_valid, message = self.validate_password(password)
            if not is_valid:
                return False, message
            
            # Check if user already exists
            if self.db and self.db.get_user_by_email(email):
                return False, "Email already registered"
            
            if self.db and self.db.get_user_by_username(username):
                return False, "Username already taken"
            
            # Hash password and create user
            password_hash = self.hash_password(password)
            
            if self.db:
                user_id = self.db.create_user(username, email, password_hash)
                if user_id:
                    return True, "User registered successfully"
                else:
                    return False, "Failed to create user"
            
            return True, "User validation passed"
            
        except Exception as e:
            return False, f"Registration error: {str(e)}"
    
    def login_user(self, email, password):
        """Authenticate user login"""
        try:
            if not self.db:
                return False, "Database not available"
            
            user = self.db.get_user_by_email(email)
            if not user:
                return False, "Invalid email or password"
            
            if self.check_password(user['password_hash'], password):
                # Create session
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['email'] = user['email']
                session['logged_in'] = True
                return True, "Login successful"
            else:
                return False, "Invalid email or password"
                
        except Exception as e:
            return False, f"Login error: {str(e)}"
    
    def logout_user(self):
        """Clear user session"""
        session.clear()
        return True, "Logged out successfully"
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return session.get('logged_in', False)
    
    def get_current_user(self):
        """Get current user info from session"""
        if self.is_logged_in():
            return {
                'id': session.get('user_id'),
                'username': session.get('username'),
                'email': session.get('email')
            }
        return None
    
    def require_login(self, f):
        """Decorator to require login for routes"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not self.is_logged_in():
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

# Global auth instance (initialize with db in your app)
auth = Auth()