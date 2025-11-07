# Combined Module Navigation Examples

## Blog + Chat Site Navigation
```html
<!-- When both blog and chat modules are active -->
<nav class="navbar">
    <a href="/">TechCommunity</a>
    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/blog">Blog</a></li>           <!-- From blog module -->
        <li><a href="/chat">Chat Rooms</a></li>     <!-- From chat module -->
        <li><a href="/direct">Direct Messages</a></li> <!-- From chat module -->
        <li><a href="/blog/write">Write Post</a></li>   <!-- From blog module -->
        <li><a href="/logout">Logout</a></li>
    </ul>
</nav>
```

## Blog + Gallery Site Navigation  
```html
<!-- When both blog and gallery modules are active -->
<nav class="navbar">
    <a href="/">Creative Portfolio</a>
    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/blog">Blog</a></li>           <!-- From blog module -->
        <li><a href="/gallery">Gallery</a></li>     <!-- From gallery module -->
        <li><a href="/blog/write">Write Post</a></li>   <!-- From blog module -->
        <li><a href="/gallery/upload">Upload</a></li>   <!-- From gallery module -->
        <li><a href="/logout">Logout</a></li>
    </ul>
</nav>
```

## Full Platform Navigation (All Modules)
```html
<!-- When blog, chat, and gallery are all active -->
<nav class="navbar">
    <a href="/">Full Platform</a>
    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/blog">Blog</a></li>
        <li><a href="/chat">Chat</a></li>
        <li><a href="/gallery">Gallery</a></li>
        <li><a href="/blog/write">Write</a></li>
        <li><a href="/chat/room/create">Create Room</a></li>
        <li><a href="/gallery/upload">Upload</a></li>
        <li><a href="/logout">Logout</a></li>
    </ul>
</nav>
```

## How Modules Detect Each Other

Each template can check if other modules are available:

```jinja2
<!-- In blog templates -->
{% if 'chat' in available_modules %}
    <li><a href="{{ url_for('chat_home') }}">Join Discussion</a></li>
{% endif %}

<!-- In chat templates -->
{% if 'blog' in available_modules %}
    <li><a href="{{ url_for('blog_home') }}">Read Articles</a></li>
{% endif %}

<!-- In any template -->
{% if 'auth' in available_modules %}
    <!-- Show login/logout options -->
{% else %}
    <!-- Hide auth-related features -->
{% endif %}
```

## Cross-Module Features

### User Experience Flow:
1. User reads a blog post
2. Clicks "Discuss in Chat" link (if chat module is active)
3. Joins a chat room to discuss the topic
4. Returns to blog to comment on the post
5. Uploads related images (if gallery module is active)

### Shared Data:
- User profiles work across all modules
- Same authentication system
- Consistent theming and styling
- Unified search (when implemented)

This modular approach lets you start simple and add features as needed!