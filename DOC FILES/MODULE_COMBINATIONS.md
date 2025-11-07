# Example 1: Blog + Chat Site (Community Platform)
app = create_app(
    modules=['blog', 'chat', 'dashboard', 'database', 'auth'], 
    config={
        'THEME': 'dark-modern',
        'DASHBOARD_TYPE': 'blog'  # Primary focus on blog
    },
    site_name='TechCommunity'
)

# Example 2: Blog + Gallery Site (Creative Portfolio)
app = create_app(
    modules=['blog', 'gallery', 'dashboard', 'database', 'auth'], 
    config={
        'THEME': 'light-professional',
        'DASHBOARD_TYPE': 'gallery'  # Primary focus on gallery
    },
    site_name='Creative Portfolio'
)

# Example 3: Full-Featured Site (All Modules)
app = create_app(
    modules=['blog', 'chat', 'gallery', 'dashboard', 'database', 'auth'], 
    config={
        'THEME': 'cyberpunk-neon',
        'DASHBOARD_TYPE': 'blog'  # Choose primary dashboard type
    },
    site_name='Full Platform'
)

# Example 4: Simple Blog Only
app = create_app(
    modules=['blog', 'dashboard', 'database', 'auth'], 
    config={
        'THEME': 'light-professional',
        'DASHBOARD_TYPE': 'blog'
    },
    site_name='Simple Blog'
)

# Example 5: Chat + Blog (Gaming Community)
app = create_app(
    modules=['chat', 'blog', 'dashboard', 'database', 'auth'], 
    config={
        'THEME': 'cyberpunk-neon',
        'DASHBOARD_TYPE': 'chat'  # Primary focus on chat
    },
    site_name='Gaming Hub'
)