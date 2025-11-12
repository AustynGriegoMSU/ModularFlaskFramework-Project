"""
Chat module for real-time messaging
Provides chat rooms, direct messages, and messaging functionality
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime

def register_chat_routes(app):
    """Register chat-related routes"""
    
    @app.route('/chat')
    def chat_home():
        """Main chat interface"""
        # Sample chat rooms
        chat_rooms = [
            {
                'id': 1,
                'name': 'General',
                'description': 'General discussion for everyone',
                'users_online': 12,
                'last_message': 'Welcome to the chat!',
                'last_activity': '2 minutes ago'
            },
            {
                'id': 2,
                'name': 'Tech Talk',
                'description': 'Programming and technology discussions',
                'users_online': 8,
                'last_message': 'Anyone working with Python?',
                'last_activity': '5 minutes ago'
            },
            {
                'id': 3,
                'name': 'Random',
                'description': 'Off-topic conversations',
                'users_online': 15,
                'last_message': 'Coffee or tea?',
                'last_activity': '1 minute ago'
            }
        ]
        
        return render_template('chat/chat.html', rooms=chat_rooms)
    
    @app.route('/chat/room/<int:room_id>')
    def chat_room(room_id):
        """Individual chat room"""
        # Sample room data
        room_info = {
            'id': room_id,
            'name': 'General' if room_id == 1 else 'Tech Talk' if room_id == 2 else 'Random',
            'description': 'Room description here',
            'users_online': 12
        }
        
        # Sample messages
        messages = [
            {
                'id': 1,
                'username': 'Alice',
                'message': 'Hey everyone!',
                'timestamp': '10:30 AM',
                'is_own_message': False
            },
            {
                'id': 2,
                'username': 'Bob',
                'message': 'How is everyone doing today?',
                'timestamp': '10:32 AM',
                'is_own_message': False
            },
            {
                'id': 3,
                'username': 'You',
                'message': 'Great! Just joined the chat',
                'timestamp': '10:35 AM',
                'is_own_message': True
            }
        ]
        
        return render_template('chat/room.html', room=room_info, messages=messages)
    
    @app.route('/chat/api/send', methods=['POST'])
    def send_message():
        """API endpoint to send a message"""
        data = request.get_json()
        message = data.get('message', '')
        room_id = data.get('room_id', 1)
        
        # Here you would save to database and broadcast to other users
        # For now, just return success
        return jsonify({
            'success': True,
            'message': message,
            'timestamp': datetime.now().strftime('%I:%M %p'),
            'username': 'You'
        })
    
    @app.route('/chat/direct')
    def direct_messages():
        """Direct message interface"""
        conversations = [
            {
                'id': 1,
                'username': 'Alice',
                'last_message': 'Thanks for the help!',
                'timestamp': '5 min ago',
                'unread_count': 2,
                'online': True
            },
            {
                'id': 2,
                'username': 'Bob',
                'last_message': 'See you tomorrow',
                'timestamp': '1 hour ago',
                'unread_count': 0,
                'online': False
            }
        ]
        
        return render_template('chat/direct.html', conversations=conversations)