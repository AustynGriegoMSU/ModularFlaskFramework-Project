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
    'chat': ['database'],           # chat requires database for message/room persistence
    'blog': ['auth', 'database'],   # blog requires auth and database
    'contact': [],                  # contact works standalone
   
}

# Backend modules that don't have routes
BACKEND_MODULES = {'database'}

def validate_dependencies(requested_modules):
    """
    Intelligent Module Dependency Validator and Auto-Resolver
    =========================================================
    
    Analyzes requested modules and automatically resolves their dependencies
    to prevent runtime errors and ensure all required functionality is loaded.
    
    This is the core innovation of the framework - it eliminates "dependency hell"
    by automatically figuring out what modules are needed and loading them in
    the correct order.
    
    Args:
        requested_modules (list): List of module names the user wants to load
                                 e.g., ['blog', 'chat'] 
    
    Returns:
        tuple: (validated_modules, warnings, errors)
               - validated_modules (list): Complete list including auto-resolved deps
               - warnings (list): Human-readable messages about auto-added modules
               - errors (list): Error messages for invalid/unknown modules
    
    Example:
        >>> validate_dependencies(['blog'])
        (['database', 'auth', 'blog'], ['Auto-added auth', 'Auto-added database'], [])
        
        This shows that requesting 'blog' automatically included its dependencies.
    """
    if not requested_modules:
        return [], [], []
    
    # Use set for O(1) lookup and automatic deduplication
    validated = set()
    warnings = []
    errors = []
    
    def add_module_with_deps(module_name, auto_added=False):
        """
        Recursively add a module and all its dependencies.
        
        Args:
            module_name (str): Name of module to add
            auto_added (bool): Whether this module was auto-added vs explicitly requested
        """
        # Skip if already processed (prevents infinite recursion)
        if module_name in validated:
            return
            
        # Validate module exists in our registry
        if module_name not in MODULE_DEPENDENCIES:
            errors.append(f"❌ Unknown module: '{module_name}'")
            return
            
        # First, recursively add all dependencies
        # This ensures dependencies are loaded before dependents
        deps = MODULE_DEPENDENCIES[module_name]
        for dep in deps:
            if dep not in validated:
                add_module_with_deps(dep, auto_added=True)
                # Only warn about auto-added deps, not explicitly requested ones
                if auto_added:
                    warnings.append(f"⚠️  Auto-added dependency '{dep}' required by '{module_name}'")
        
        # Finally, add the module itself to our validated set
        validated.add(module_name)
    
    # Process all explicitly requested modules
    # Each will recursively pull in its dependencies
    for module in requested_modules:
        add_module_with_deps(module, auto_added=False)
    
    # Return as list (ordered), plus human-readable feedback
    return list(validated), warnings, errors

def create_app(modules=None, config=None, site_name=None):
    """
    Flask Application Factory with Intelligent Module Loading
    ========================================================
    
    The main entry point for creating Flask applications with modular architecture.
    This factory function handles dependency resolution, configuration, and module
    initialization to create production-ready web applications.
    
    Key Features:
    - Automatic dependency resolution (request 'blog' → gets 'auth' + 'database')
    - Intelligent console output showing exactly what's loaded and why
    - Safe template helpers (urls that don't break when modules missing)
    - Flexible configuration system
    - Production-ready defaults with development-friendly debugging
    
    Args:
        modules (list, optional): List of module names to load. 
                                 Dependencies will be auto-resolved.
                                 Available: 'auth', 'blog', 'chat', 'dashboard', 
                                           'database', 'main', 'contact'
                                 
        config (dict, optional): Configuration overrides for Flask app.
                                Common options:
                                - 'THEME': 'light-professional', 'dark-modern', 
                                          'cyberpunk-neon', 'space-animated'
                                - 'DASHBOARD_TYPE': 'default', 'blog', 'chat'
                                - 'DATABASE_PATH': custom database file location
                                - 'SECRET_KEY': for production security
                                
        site_name (str, optional): Display name for the application.
                                  Used in templates and page titles.
    
    Returns:
        Flask: Configured Flask application instance ready to run
    
    Raises:
        ValueError: If module dependencies cannot be resolved or unknown modules specified
        
    Note:
        The function provides detailed console output showing dependency resolution,
        theme selection, and module loading status. This helps with debugging and
        understanding what functionality is available.
    """
    from flask import Flask
    import os
    
    # ========================================================================
    # STEP 1: INTELLIGENT MODULE DEPENDENCY RESOLUTION
    # ========================================================================
    # Analyze requested modules and automatically include any missing dependencies
    # This prevents runtime errors and ensures all required functionality is available
    if modules:
        validated_modules, warnings, errors = validate_dependencies(modules)
        
        # Provide detailed console feedback for developer awareness
        # This helps users understand what's being loaded and why
        print("🔧 MODULE DEPENDENCY ANALYSIS")
        print("=" * 40)
        print(f"📋 Requested: {modules}")
        print(f"✅ Loading: {validated_modules}")
        
        # Show any auto-resolved dependencies with explanatory warnings
        if warnings:
            print("\n⚠️  DEPENDENCY WARNINGS:")
            for warning in warnings:
                print(f"   {warning}")
        
        # Halt execution if invalid modules specified - fail fast principle
        if errors:
            print("\n❌ DEPENDENCY ERRORS:")
            for error in errors:
                print(f"   {error}")
            raise ValueError("Module dependency validation failed. Check errors above.")
        
        # Highlight any modules that were auto-added for transparency
        if set(validated_modules) != set(modules):
            auto_added = set(validated_modules) - set(modules)
            print(f"\n🔄 Auto-resolved dependencies: {auto_added}")
        
        print("=" * 40)
        modules = validated_modules
    else:
        # Handle case where no modules specified - create minimal Flask app
        modules = []
    
    # ========================================================================
    # STEP 2: FLASK APPLICATION SETUP WITH PROPER FOLDER STRUCTURE  
    # ========================================================================
    # Configure Flask with proper paths for templates, static files, and data storage
    project_root = os.path.dirname(os.path.dirname(__file__))
    instance_path = os.path.join(project_root, 'instance')     # For database and user data
    static_path = os.path.join(project_root, 'static')         # For CSS, JS, images
    template_path = os.path.join(project_root, 'templates')    # For HTML templates
    
    # Ensure data directory exists - Flask won't create it automatically
    os.makedirs(instance_path, exist_ok=True)
    
    # Initialize Flask with explicit paths for predictable behavior across environments
    app = Flask(__name__, 
                template_folder=template_path,      # HTML templates location
                static_folder=static_path,          # CSS/JS/images location  
                instance_path=instance_path,        # Private data storage
                instance_relative_config=True)     # Enable config files in instance/
    
    # ========================================================================
    # STEP 3: APPLICATION CONFIGURATION WITH SENSIBLE DEFAULTS
    # ========================================================================
    # Set up Flask configuration with production-ready defaults that can be overridden
    app.config.update({
        # Security configuration
        'SECRET_KEY': 'change-this-in-production',     # MUST be changed for production
        
        # Development settings  
        'DEBUG': True,                                 # Disable in production
        
        # Database configuration
        'DATABASE_PATH': os.path.join(instance_path, 'app.db'),  # SQLite in instance folder
        
        # Theme and UI configuration
        'THEME': 'light-professional',                 # Default professional appearance
        'CACHE_BUSTER': '1.3',                        # Increment to force CSS reload
        'DASHBOARD_TYPE': 'default',                   # Dashboard variant to show
        
        # Application metadata
        'SITE_NAME': site_name,                        # Display name for templates
        'MODULES': modules or [],                      # Track loaded modules for debugging
    })
    
    # Override defaults with user-provided configuration
    if config:
        app.config.update(config)    # Show theme, site, and dashboard information
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
        # Initialize database with Flask app's configured path
        app.db = DatabaseManager(app.config.get('DATABASE_PATH'))
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