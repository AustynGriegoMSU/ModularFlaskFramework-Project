"""
Blog module for content management
Provides blog posts, categories, comments, and publishing functionality
"""

from flask import render_template, request, redirect, url_for, flash, abort
from datetime import datetime

def register_blog_routes(app):
    """Register blog-related routes"""
    
    @app.route('/blog')
    def blog_home():
        """Main blog listing page"""
        # If database module is available, load posts from DB; otherwise use sample posts
        if hasattr(app, 'db') and app.db:
            try:
                posts = app.db.get_posts(limit=20)
            except Exception:
                posts = []
        else:
            # Sample blog posts
            posts = [
            {
                'id': 1,
                'title': 'Getting Started with Python',
                'excerpt': 'A comprehensive guide for beginners to learn Python programming from scratch.',
                'author': 'John Doe',
                'date': '2025-11-05',
                'category': 'Programming',
                'tags': ['python', 'beginner', 'tutorial'],
                'views': 234,
                'comments': 12,
                'featured_image': '/static/blog1.jpg',
                'published': True
            },
            {
                'id': 2,
                'title': 'Web Development Best Practices',
                'excerpt': 'Essential tips and tricks for modern web development that every developer should know.',
                'author': 'Jane Smith',
                'date': '2025-11-04',
                'category': 'Web Development',
                'tags': ['web', 'best-practices', 'tips'],
                'views': 189,
                'comments': 8,
                'featured_image': '/static/blog2.jpg',
                'published': True
            },
            {
                'id': 3,
                'title': 'Database Design Fundamentals',
                'excerpt': 'Understanding the principles of good database architecture and design patterns.',
                'author': 'Mike Johnson',
                'date': '2025-11-03',
                'category': 'Database',
                'tags': ['database', 'design', 'sql'],
                'views': 156,
                'comments': 5,
                'featured_image': '/static/blog3.jpg',
                'published': True
            }
        ]
        
        # Sample categories
        if hasattr(app, 'db') and app.db:
            # derive categories from posts if possible
            cats = {}
            for p in posts:
                c = p.get('category') or 'Uncategorized'
                cats[c] = cats.get(c, 0) + 1
            categories = [{'name': k, 'count': v} for k, v in sorted(cats.items(), key=lambda x: -x[1])]
        else:
            categories = [
                {'name': 'Programming', 'count': 8},
                {'name': 'Web Development', 'count': 6},
                {'name': 'Database', 'count': 4},
                {'name': 'Tutorials', 'count': 12},
                {'name': 'Reviews', 'count': 3}
            ]
        
        return render_template('blog/blog.html', posts=posts, categories=categories)
    
    @app.route('/blog/post/<int:post_id>')
    def blog_post(post_id):
        """Individual blog post view"""
        # Try to fetch post from DB if available
        if hasattr(app, 'db') and app.db:
            post = app.db.get_post_by_id(post_id)
            comments = []
            related_posts = []
            if not post:
                abort(404)
        else:
            # Fallback sample post
            post = {
                'id': post_id,
                'title': 'Getting Started with Python',
                'content': '''
                <p>Python is an excellent programming language for beginners and experienced developers alike. In this comprehensive guide, we'll explore the fundamentals of Python programming.</p>
                ''',
                'author': 'John Doe',
                'date': '2025-11-05',
                'category': 'Programming',
                'tags': ['python', 'beginner', 'tutorial'],
                'views': 234,
                'featured_image': '/static/blog1.jpg'
            }
            comments = [
                {
                    'id': 1,
                    'author': 'Alice',
                    'content': 'Great tutorial! This really helped me understand Python basics.',
                    'date': '2025-11-05 14:30',
                    'avatar': '/static/avatar1.jpg'
                }
            ]
            related_posts = []

        return render_template('blog/post.html', post=post, comments=comments, related_posts=related_posts)
    
    @app.route('/blog/category/<category_name>')
    def blog_category(category_name):
        """Posts by category"""
        if hasattr(app, 'db') and app.db:
            # simple filter using search helper
            posts = [p for p in app.db.get_posts(limit=100) if (p.get('category') or '').lower() == category_name.lower()]
        else:
            posts = [
                {
                    'id': 1,
                    'title': 'Getting Started with Python',
                    'excerpt': 'A comprehensive guide for beginners.',
                    'author': 'John Doe',
                    'date': '2025-11-05',
                    'views': 234,
                    'comments': 12
                }
            ]

        return render_template('blog/category.html', posts=posts, category=category_name)
    
    @app.route('/blog/write', methods=['GET', 'POST'])
    def blog_write():
        """Create new blog post (requires auth)"""
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            category = request.form.get('category')
            tags = request.form.get('tags')
            # Try to save to database if available
            if hasattr(app, 'db') and app.db:
                post_id = app.db.create_post(title=title, content=content, author=(request.form.get('author') or 'Guest'), category=category, tags=[t.strip() for t in (tags or '').split(',') if t.strip()])
                if post_id:
                    flash('Post created successfully!', 'success')
                    return redirect(url_for('blog_post', post_id=post_id))
                else:
                    flash('Failed to create post', 'error')
            else:
                flash('Database not enabled; post not saved', 'error')
            return redirect(url_for('blog_home'))
        
        return render_template('blog/write.html')
    
    @app.route('/blog/search')
    def blog_search():
        """Search blog posts"""
        query = request.args.get('q', '')
        if hasattr(app, 'db') and app.db and query:
            posts = app.db.search_posts(query)
        else:
            posts = []
        return render_template('blog/search.html', posts=posts, query=query)