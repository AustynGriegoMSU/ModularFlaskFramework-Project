"""
Route modules for common Flask functionality
"""

from flask import render_template, request, redirect, url_for, flash
from . import auth
from .modules.chat import register_chat_routes
from .modules.blog import register_blog_routes

def register_auth_routes(app):
    """Register authentication routes"""
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form.get('confirm_password', '')
            
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return render_template('auth/register.html')
            
            success, message = auth.register_user(username, email, password)
            if success:
                flash(message, 'success')
                return redirect(url_for('login'))
            else:
                flash(message, 'error')
        
        return render_template('auth/register.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            
            success, message = auth.login_user(email, password)
            if success:
                flash(message, 'success')
                return redirect(url_for('dashboard'))
            else:
                flash(message, 'error')
        
        return render_template('auth/login.html')
    
    @app.route('/logout')
    def logout():
        auth.logout_user()
        flash('You have been logged out', 'info')
        return redirect(url_for('index'))

def register_dashboard_routes(app):
    """Register dashboard routes (works with or without auth module)"""
    # Register dashboard route and let the configuration choose which
    # dashboard variant to render. This avoids depending on whether auth
    # routes were registered earlier and makes the dashboard_type config
    # the single source of truth.
    @app.route('/dashboard')
    @app.route('/')  # Make dashboard the home page too
    def dashboard():
        # Choose dashboard type based on app config
        dashboard_type = app.config.get('DASHBOARD_TYPE', 'default')
        print(f"📊 LOADING DASHBOARD: {dashboard_type}")

        if dashboard_type == 'chat':
            # Chat site stats
            stats = {
                'total_messages': 247,
                'active_chats': 5,
                'unread_messages': 3,
                'online_friends': 12
            }

            recent_activity = [
                {
                    'title': 'General Chat',
                    'description': 'Join the community discussion',
                    'timestamp': '2 minutes ago',
                    'type': 'chat'
                },
                {
                    'title': 'Tech Talk',
                    'description': 'Latest programming discussions',
                    'timestamp': '15 minutes ago',
                    'type': 'chat'
                }
            ]

            return render_template('dashboard/chat-dashboard.html',
                                 stats=stats,
                                 recent_activity=recent_activity)

        elif dashboard_type == 'gallery':
            # Gallery site stats
            stats = {
                'total_photos': 342,
                'albums': 8,
                'favorites': 23,
                'storage_used': '67%'
            }

            recent_activity = [
                {
                    'title': 'Vacation 2025',
                    'description': 'Beach photos from summer trip',
                    'timestamp': '1 hour ago',
                    'type': 'photo'
                },
                {
                    'title': 'City Lights',
                    'description': 'Night photography collection',
                    'timestamp': '3 hours ago',
                    'type': 'photo'
                }
            ]

            return render_template('dashboard/gallery-dashboard.html',
                                 stats=stats,
                                 recent_activity=recent_activity)

        elif dashboard_type == 'blog':
            # Blog site stats
            stats = {
                'total_posts': 24,
                'draft_posts': 3,
                'total_views': 1847,
                'comments': 89
            }

            recent_activity = [
                {
                    'title': 'Getting Started with Python',
                    'description': 'A comprehensive guide for beginners to learn Python programming',
                    'timestamp': '2 hours ago',
                    'views': 156,
                    'comments': 12,
                    'type': 'blog'
                },
                {
                    'title': 'Web Development Best Practices',
                    'description': 'Essential tips and tricks for modern web development',
                    'timestamp': '1 day ago',
                    'views': 234,
                    'comments': 18,
                    'type': 'blog'
                },
                {
                    'title': 'Database Design Fundamentals',
                    'description': 'Understanding the principles of good database architecture',
                    'timestamp': '3 days ago',
                    'views': 189,
                    'comments': 7,
                    'type': 'blog'
                }
            ]

            return render_template('dashboard/blog-dashboard.html',
                                 stats=stats,
                                 recent_activity=recent_activity)

        else:
            # Default item tracker dashboard
            stats = {
                'total_items': 15,
                'active_items': 8,
                'pending_items': 4,
                'completed_items': 3
            }

            recent_activity = [
                {
                    'title': 'Welcome!',
                    'description': 'Dashboard loaded successfully',
                    'timestamp': 'Just now',
                    'type': 'system'
                }
            ]

            return render_template('dashboard/dashboard.html',
                                 stats=stats,
                                 recent_activity=recent_activity)

def register_main_routes(app):
    """Register main/basic routes"""
    
    @app.route('/')
    @app.route('/home')
    def index():
        return render_template('main/index.html')
    
    @app.route('/about')
    def about():
        return render_template('main/about.html')
    
    @app.route('/contact')
    def contact():
        return render_template('main/contact.html')

# Route registry
ROUTE_MODULES = {
    'auth': register_auth_routes,
    'dashboard': register_dashboard_routes,
    'main': register_main_routes,
    'chat': register_chat_routes,
    'blog': register_blog_routes,
}