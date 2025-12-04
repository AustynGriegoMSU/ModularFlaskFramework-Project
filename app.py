"""
Main application file
Uses the modular Flask framework from library/
"""

from library import create_app

app = create_app(
        modules=['chat', 'database', 'dashboard', 'auth'], 
        config={
            'THEME': 'cyberpunk-neon',
            'DASHBOARD_TYPE': 'chat',  
        },
        site_name='Project Chat Demo'
    )

# Debug route to check theme and dashboard
@app.route('/debug')
def debug():
    dashboard_type = app.config.get('DASHBOARD_TYPE', 'default')
    modules_list = ', '.join(app.config.get('MODULES', []))
    
    return f"""
    <h1>🔧 Flask App Debug Info</h1>
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; font-family: monospace;">
        <h2>📊 Dashboard Configuration</h2>
        <p><strong>Dashboard Type:</strong> <span style="color: #007bff; font-size: 1.2em;">{dashboard_type}</span></p>
        <p><strong>Dashboard Template:</strong> templates/dashboard/{dashboard_type}-dashboard.html</p>
        <p><strong>Active Modules:</strong> {modules_list}</p>
        
        <h2>🎨 Theme Configuration</h2>
        <p><strong>Theme:</strong> {app.config.get('THEME')}</p>
        <p><strong>Cache Buster:</strong> {app.config.get('CACHE_BUSTER')}</p>
        <p><strong>CSS URL:</strong> /static/{app.config.get('THEME')}.css?v={app.config.get('CACHE_BUSTER')}</p>
        
        <h2>🏷️ Site Information</h2>
        <p><strong>Site Name:</strong> {app.config.get('SITE_NAME')}</p>
        
        <h2>🔗 Quick Links</h2>
        <p><a href="/" style="color: #007bff;">← Back to Dashboard</a></p>
        <p><a href="/static/{app.config.get('THEME')}.css?v={app.config.get('CACHE_BUSTER')}" target="_blank">View CSS File →</a></p>
    </div>
    """

if __name__ == '__main__':
    app.run(debug=True)