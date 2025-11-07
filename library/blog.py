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
        # Sample post data (in real app, fetch from database)
        post = {
            'id': post_id,
            'title': 'Getting Started with Python',
            'content': '''
            <p>Python is an excellent programming language for beginners and experienced developers alike. In this comprehensive guide, we'll explore the fundamentals of Python programming.</p>
            
            <h3>Why Choose Python?</h3>
            <p>Python offers several advantages:</p>
            <ul>
                <li>Simple and readable syntax</li>
                <li>Extensive standard library</li>
                <li>Large community support</li>
                <li>Versatile applications</li>
            </ul>
            
            <h3>Getting Started</h3>
            <p>To begin your Python journey, you'll need to install Python on your system. Visit the official Python website and download the latest version.</p>
            
            <pre><code>print("Hello, World!")</code></pre>
            
            <p>This simple program demonstrates Python's clean syntax. Unlike other languages, Python doesn't require semicolons or complex syntax structures.</p>
            ''',
            'author': 'John Doe',
            'date': '2025-11-05',
            'category': 'Programming',
            'tags': ['python', 'beginner', 'tutorial'],
            'views': 234,
            'featured_image': '/static/blog1.jpg'
        }
        
        # Sample comments
        comments = [
            {
                'id': 1,
                'author': 'Alice',
                'content': 'Great tutorial! This really helped me understand Python basics.',
                'date': '2025-11-05 14:30',
                'avatar': '/static/avatar1.jpg'
            },
            {
                'id': 2,
                'author': 'Bob',
                'content': 'Very clear explanations. Looking forward to more advanced topics!',
                'date': '2025-11-05 16:45',
                'avatar': '/static/avatar2.jpg'
            }
        ]
        
        # Related posts
        related_posts = [
            {
                'id': 4,
                'title': 'Python Data Types Explained',
                'excerpt': 'Understanding strings, lists, dictionaries, and more.',
                'date': '2025-11-04'
            },
            {
                'id': 5,
                'title': 'Python Functions and Modules',
                'excerpt': 'Learn how to organize your Python code effectively.',
                'date': '2025-11-03'
            }
        ]
        
        return render_template('blog/post.html', post=post, comments=comments, related_posts=related_posts)
    
    @app.route('/blog/category/<category_name>')
    def blog_category(category_name):
        """Posts by category"""
        # Sample filtered posts
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
            
            # In real app, save to database
            flash('Post created successfully!', 'success')
            return redirect(url_for('blog_home'))
        
        return render_template('blog/write.html')
    
    @app.route('/blog/search')
    def blog_search():
        """Search blog posts"""
        query = request.args.get('q', '')
        
        # Sample search results
        if query:
            posts = [
                {
                    'id': 1,
                    'title': 'Getting Started with Python',
                    'excerpt': 'A comprehensive guide for beginners.',
                    'author': 'John Doe',
                    'date': '2025-11-05',
                    'highlight': 'Python programming tutorial'
                }
            ]
        else:
            posts = []
        
        return render_template('blog/search.html', posts=posts, query=query)