"""
SQL Database module for Project L
Handles database connections, user management, and data operations
"""

import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            # Use instance folder for database
            instance_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
            os.makedirs(instance_dir, exist_ok=True)
            self.db_path = os.path.join(instance_dir, 'project_l.db')
        else:
            self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database with required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # User sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_token TEXT UNIQUE NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    expires_at DATETIME NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # User profiles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE NOT NULL,
                    first_name TEXT,
                    last_name TEXT,
                    bio TEXT,
                    avatar_url TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()

            # Blog posts table (optional for blog module)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    author TEXT,
                    category TEXT,
                    tags TEXT,
                    featured_image TEXT,
                    views INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    published BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()
    
    def create_user(self, username, email, password_hash):
        """Create a new user"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, email, password_hash)
                    VALUES (?, ?, ?)
                ''', (username, email, password_hash))
                
                user_id = cursor.lastrowid
                
                # Create default profile
                cursor.execute('''
                    INSERT INTO user_profiles (user_id)
                    VALUES (?)
                ''', (user_id,))
                
                conn.commit()
                return user_id
        except sqlite3.IntegrityError:
            return None
        except Exception as e:
            print(f"Database error: {e}")
            return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM users WHERE id = ? AND is_active = 1
            ''', (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM users WHERE email = ? AND is_active = 1
            ''', (email,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_user_by_username(self, username):
        """Get user by username"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM users WHERE username = ? AND is_active = 1
            ''', (username,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_user(self, user_id, **kwargs):
        """Update user information"""
        if not kwargs:
            return False
        
        # Build dynamic update query
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [user_id]
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f'''
                    UPDATE users 
                    SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', values)
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Update error: {e}")
            return False
    
    def delete_user(self, user_id):
        """Soft delete user (mark as inactive)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users 
                    SET is_active = 0, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (user_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Delete error: {e}")
            return False
    
    def get_user_profile(self, user_id):
        """Get user profile"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT u.*, p.first_name, p.last_name, p.bio, p.avatar_url
                FROM users u
                LEFT JOIN user_profiles p ON u.id = p.user_id
                WHERE u.id = ? AND u.is_active = 1
            ''', (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_user_profile(self, user_id, **profile_data):
        """Update user profile"""
        if not profile_data:
            return False
        
        set_clause = ", ".join([f"{key} = ?" for key in profile_data.keys()])
        values = list(profile_data.values()) + [user_id]
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f'''
                    UPDATE user_profiles 
                    SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', values)
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Profile update error: {e}")
            return False
    
    def get_all_users(self, limit=100, offset=0):
        """Get all active users with pagination"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT u.id, u.username, u.email, u.created_at,
                       p.first_name, p.last_name
                FROM users u
                LEFT JOIN user_profiles p ON u.id = p.user_id
                WHERE u.is_active = 1
                ORDER BY u.created_at DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            return [dict(row) for row in cursor.fetchall()]
    
    def search_users(self, query, limit=50):
        """Search users by username or email"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            search_term = f"%{query}%"
            cursor.execute('''
                SELECT u.id, u.username, u.email,
                       p.first_name, p.last_name
                FROM users u
                LEFT JOIN user_profiles p ON u.id = p.user_id
                WHERE u.is_active = 1 
                AND (u.username LIKE ? OR u.email LIKE ? 
                     OR p.first_name LIKE ? OR p.last_name LIKE ?)
                ORDER BY u.username
                LIMIT ?
            ''', (search_term, search_term, search_term, search_term, limit))
            return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """Close database connection (for cleanup)"""
        # Using context manager, so no persistent connection to close
        pass

    # Simple blog helpers
    def create_post(self, title, content, author=None, category=None, tags=None, featured_image=None, published=True):
        tags_str = ','.join(tags) if isinstance(tags, (list, tuple)) else (tags or '')
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO posts (title, content, author, category, tags, featured_image, published)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (title, content, author, category, tags_str, featured_image, 1 if published else 0))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Create post error: {e}")
            return None

    def get_posts(self, limit=20, offset=0):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM posts WHERE published = 1
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            return [dict(row) for row in cursor.fetchall()]

    def get_post_by_id(self, post_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM posts WHERE id = ? AND published = 1
            ''', (post_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def search_posts(self, query, limit=20):
        search_term = f"%{query}%"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM posts WHERE published = 1 AND (title LIKE ? OR content LIKE ? OR tags LIKE ?)
                ORDER BY created_at DESC
                LIMIT ?
            ''', (search_term, search_term, search_term, limit))
            return [dict(row) for row in cursor.fetchall()]

# Global database instance
db = DatabaseManager()