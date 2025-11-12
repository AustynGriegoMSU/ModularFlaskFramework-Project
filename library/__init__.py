"""
Modular Flask Library
Contains reusable modules for rapid Flask development
"""

from flask import Flask, url_for
from .modules.auth import Auth, auth
from .modules.database import DatabaseManager, db
from .routes import ROUTE_MODULES

# Module dependency definitions
MODULE_DEPENDENCIES = {
    'auth': ['database'],           # auth requires database
    'dashboard': [],                # dashboard works standalone but enhanced by auth
    'main': [],                     # main is standalone
    'database': [],                 # database is a backend module (no routes)
    'chat': [],                     # chat works standalone (enhanced by auth)
    'blog': ['auth', 'database'],   # blog requires auth and database
    'forum': ['auth', 'database'],  # forum requires auth and database
    'ecommerce': ['auth', 'database'], # ecommerce requires auth and database
    'gallery': ['auth'],            # gallery requires auth for uploads
    'contact': [],                  # contact works standalone
    'search': [],                   # search is standalone
    'events': ['auth', 'database'], # events require auth and database
}

# Backend modules that don't have routes
BACKEND_MODULES = {'database'}

def validate_dependencies(requested_modules):
    """
    Validate and auto-resolve module dependencies
    Returns: (validated_modules, warnings, errors)
    """
    if not requested_modules:
        return [], [], []
    
    validated = set()
    warnings = []
    errors = []
    
    def add_module_with_deps(module_name, auto_added=False):
        if module_name in validated:
            return
            
        if module_name not in MODULE_DEPENDENCIES:
            errors.append(f"❌ Unknown module: '{module_name}'")
            return
            
        # Add dependencies first
        deps = MODULE_DEPENDENCIES[module_name]
        for dep in deps:
            if dep not in validated:
                add_module_with_deps(dep, auto_added=True)
                if auto_added:
                    warnings.append(f"⚠️  Auto-added dependency '{dep}' required by '{module_name}'")
        
        validated.add(module_name)
    
    # Process all requested modules
    for module in requested_modules:
        add_module_with_deps(module, auto_added=False)
    
    return list(validated), warnings, errors

def create_app(modules=None, config=None, site_name=None):
    """
    Create Flask app with selected modules
    
    Automatically resolves and loads module dependencies.
    
    Usage:
        from library import create_app
        app = create_app(modules=['dashboard', 'auth'], site_name='My Custom App')
    """
    from flask import Flask
    import os
    
    # Validate and resolve dependencies
    if modules:
        validated_modules, warnings, errors = validate_dependencies(modules)
        
        # Print dependency information
        print("🔧 MODULE DEPENDENCY ANALYSIS")
        print("=" * 40)
        print(f"📋 Requested: {modules}")
        print(f"✅ Loading: {validated_modules}")
        
        if warnings:
            print("\n⚠️  DEPENDENCY WARNINGS:")
            for warning in warnings:
                print(f"   {warning}")
        
        if errors:
            print("\n❌ DEPENDENCY ERRORS:")
            for error in errors:
                print(f"   {error}")
            raise ValueError("Module dependency validation failed. Check errors above.")
        
        if set(validated_modules) != set(modules):
            print(f"\n🔄 Auto-resolved dependencies: {set(validated_modules) - set(modules)}")
        
        print("=" * 40)
        modules = validated_modules
    else:
        modules = []
    
    # Create Flask app with proper instance folder configuration
    instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
    static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    os.makedirs(instance_path, exist_ok=True)
    
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
                static_folder=static_path,
                instance_path=instance_path,
                instance_relative_config=True)
    
    # Default config
    app.config.update({
        'SECRET_KEY': 'change-this-in-production',
        'DEBUG': True,
        'DATABASE_PATH': os.path.join(instance_path, 'project_l.db'),
        'THEME': 'light-professional',  # Default theme
        'CACHE_BUSTER': '1.3',  # Increment to force CSS reload
        'SITE_NAME': site_name,  # Site name for templates - no default fallback
        'MODULES': modules or []  # Store active modules for debug info
    })
    
    if config:
        app.config.update(config)
    
    # Show theme, site, and dashboard information
    theme = app.config.get('THEME', 'light-professional')
    site_name_display = app.config.get('SITE_NAME') or 'Unnamed Project'
    dashboard_type = app.config.get('DASHBOARD_TYPE', 'default')
    
    print(f"🎨 THEME: {theme}")
    print(f"🏷️  SITE: {site_name_display}")
    print(f"📊 DASHBOARD: {dashboard_type}")
    print("=" * 40)
    
    # Initialize selected modules
    # Database must be loaded first if needed
    if 'database' in modules:
        app.db = db
        print("✅ Database module loaded")

    # Always provide module info and safe URL building so templates can
    # safely reference module routes even if those modules are not enabled.
    @app.context_processor
    def inject_helpers():
        def safe_url_for(endpoint, **values):
            """Safely build URL, return '#' if route doesn't exist"""
            try:
                return url_for(endpoint, **values)
            except:
                return '#'

        result = {
            'available_modules': modules,
            'safe_url_for': safe_url_for,
            'current_user': None
        }

        # Add current_user if auth module is loaded
        if 'auth' in modules:
            try:
                user = auth.get_current_user()
                # If no user or user is None, provide Guest fallback
                result['current_user'] = user if user else {'username': 'Guest'}
            except Exception:
                result['current_user'] = {'username': 'Guest'}
        else:
            result['current_user'] = {'username': 'Guest'}

        return result

    if 'auth' in modules:
        auth.db = db
        print("✅ Auth module loaded")

    # Register routes for each module (skip backend modules)
    for module_name in modules:
        if module_name in BACKEND_MODULES:
            print(f"✅ {module_name.title()} backend module loaded")
        elif module_name in ROUTE_MODULES:
            ROUTE_MODULES[module_name](app)
            print(f"✅ {module_name.title()} routes registered")
        else:
            print(f"⚠️  Warning: {module_name} module not found in route registry")
    
    return app

__all__ = ['Auth', 'auth', 'DatabaseManager', 'db', 'create_app']