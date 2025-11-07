"""
Quick App Configurations
Switch between different app types by changing the configuration
"""

from library import create_app

# 1. TECH BLOG + COMMUNITY CHAT
def create_tech_community():
    return create_app(
        modules=['blog', 'chat', 'dashboard', 'database', 'auth'], 
        config={
            'THEME': 'dark-modern',
            'DASHBOARD_TYPE': 'blog'  # Blog-focused with chat features
        },
        site_name='Tech Community'
    )

# 2. CREATIVE PORTFOLIO + BLOG
def create_creative_portfolio():
    return create_app(
        modules=['blog', 'gallery', 'dashboard', 'database', 'auth'], 
        config={
            'THEME': 'light-professional',
            'DASHBOARD_TYPE': 'gallery'  # Gallery-focused with blog features
        },
        site_name='Creative Portfolio'
    )

# 3. GAMING HUB (Chat + Blog)
def create_gaming_hub():
    return create_app(
        modules=['chat', 'blog', 'dashboard', 'database', 'auth'], 
        config={
            'THEME': 'cyberpunk-neon',
            'DASHBOARD_TYPE': 'chat'  # Chat-focused with blog features
        },
        site_name='Gaming Hub'
    )

# 4. SIMPLE BLOG ONLY
def create_simple_blog():
    return create_app(
        modules=['blog', 'dashboard', 'database', 'auth'], 
        config={
            'THEME': 'light-professional',
            'DASHBOARD_TYPE': 'blog'
        },
        site_name='My Blog'
    )

# 5. FULL-FEATURED PLATFORM
def create_full_platform():
    return create_app(
        modules=['blog', 'chat', 'gallery', 'dashboard', 'database', 'auth'], 
        config={
            'THEME': 'dark-modern',
            'DASHBOARD_TYPE': 'blog'  # Choose your primary focus
        },
        site_name='Full Platform'
    )

# Choose which app to run:
app = create_tech_community()  # <-- Change this line to switch apps

# Or use conditional logic:
import os
APP_TYPE = os.environ.get('APP_TYPE', 'blog')

if APP_TYPE == 'community':
    app = create_tech_community()
elif APP_TYPE == 'portfolio':
    app = create_creative_portfolio()
elif APP_TYPE == 'gaming':
    app = create_gaming_hub()
elif APP_TYPE == 'full':
    app = create_full_platform()
else:
    app = create_simple_blog()

if __name__ == '__main__':
    app.run(debug=True)