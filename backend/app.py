from flask import Flask, request, jsonify, send_file
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, timedelta
import json
import os
from models import db, User, Message, ChatRoom, UserChatRoom
from utils.authentication import hash_password, verify_password
from utils.payment_processor import process_payment
from utils.file_upload import save_uploaded_file
from ai_integration import AIChatAssistant

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Initialize extensions
db.init_app(app)
CORS(app)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Initialize AI assistant
ai_assistant = AIChatAssistant(app.config['OPENAI_API_KEY'])

@app.route('/')
def index():
    return jsonify({"status": "Chat API is running", "version": "1.0.0"})

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "User already exists"}), 400
        
        # Create new user
        hashed_password = hash_password(data['password'])
        new_user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hashed_password,
            phone_number=data.get('phone_number'),
            country=data.get('country', 'US')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=new_user.id)
        
        return jsonify({
            "message": "User created successfully",
            "user_id": new_user.id,
            "access_token": access_token
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not verify_password(data['password'], user.password_hash):
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            "message": "Login successful",
            "user_id": user.id,
            "access_token": access_token,
            "username": user.username
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403
            
        user = User.query.get_or_404(user_id)
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number,
            "country": user.country,
            "credits": user.credits,
            "created_at": user.created_at.isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/contacts', methods=['GET'])
@jwt_required()
def get_contacts():
    try:
        current_user_id = get_jwt_identity()
        
        # Get all users except the current user
        contacts = User.query.filter(User.id != current_user_id).all()
        
        contacts_data = []
        for contact in contacts:
            # Get the last message between current user and this contact
            last_message = Message.query.filter(
                ((Message.sender_id == current_user_id) & (Message.receiver_id == contact.id)) |
                ((Message.sender_id == contact.id) & (Message.receiver_id == current_user_id))
            ).order_by(Message.timestamp.desc()).first()
            
            contacts_data.append({
                "id": contact.id,
                "username": contact.username,
                "avatar": contact.avatar,
                "last_message": last_message.content if last_message else "No messages yet",
                "last_message_time": last_message.timestamp.isoformat() if last_message else None,
                "unread_count": Message.query.filter_by(
                    sender_id=contact.id, 
                    receiver_id=current_user_id,
                    read=False
                ).count()
            })
        
        return jsonify(contacts_data), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/messages/<int:contact_id>', methods=['GET'])
@jwt_required()
def get_messages(contact_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Get messages between current user and the contact
        messages = Message.query.filter(
            ((Message.sender_id == current_user_id) & (Message.receiver_id == contact_id)) |
            ((Message.sender_id == contact_id) & (Message.receiver_id == current_user_id))
        ).order_by(Message.timestamp.asc()).all()
        
        # Mark messages as read
        Message.query.filter_by(sender_id=contact_id, receiver_id=current_user_id, read=False).update(
            {Message.read: True}, synchronize_session=False
        )
        db.session.commit()
        
        messages_data = []
        for msg in messages:
            messages_data.append({
                "id": msg.id,
                "sender_id": msg.sender_id,
                "receiver_id": msg.receiver_id,
                "content": msg.content,
                "message_type": msg.message_type,
                "timestamp": msg.timestamp.isoformat(),
                "read": msg.read
            })
        
        return jsonify(messages_data), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/upload', methods=['POST'])
@jwt_required()
def upload_file():
    try:
        current_user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
            
        # Save the file
        file_path = save_uploaded_file(file, current_user_id)
        
        return jsonify({
            "message": "File uploaded successfully",
            "file_path": file_path
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/payment/process', methods=['POST'])
@jwt_required()
def process_payment_route():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Process payment
        result = process_payment(
            user_id=current_user_id,
            amount=data['amount'],
            currency=data['currency'],
            payment_method=data['payment_method'],
            card_token=data.get('card_token')
        )
        
        if result['success']:
            # Add credits to user
            user = User.query.get(current_user_id)
            user.credits += data['credits']
            db.session.commit()
            
            return jsonify({
                "message": "Payment processed successfully",
                "credits_added": data['credits'],
                "new_balance": user.credits
            }), 200
        else:
            return jsonify({"error": result['message']}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connected', {'data': 'Connected to chat server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join_chat')
@jwt_required()
def handle_join_chat(data):
    try:
        user_id = get_jwt_identity()
        room = f"chat_{data['contact_id']}_{user_id}" if 'contact_id' in data else f"user_{user_id}"
        join_room(room)
        emit('joined_room', {'room': room})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('send_message')
@jwt_required()
def handle_send_message(data):
    try:
        user_id = get_jwt_identity()
        
        # AI content moderation
        moderation_result = ai_assistant.moderate_content(data['content'])
        if moderation_result['flagged']:
            emit('message_blocked', {
                'message': 'Message contains inappropriate content',
                'reason': moderation_result['reason']
            })
            return
        
        # Create new message
        new_message = Message(
            sender_id=user_id,
            receiver_id=data['receiver_id'],
            content=data['content'],
            message_type=data.get('type', 'text')
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        # Prepare message data for emission
        message_data = {
            'id': new_message.id,
            'sender_id': new_message.sender_id,
            'receiver_id': new_message.receiver_id,
            'content': new_message.content,
            'message_type': new_message.message_type,
            'timestamp': new_message.timestamp.isoformat(),
            'read': new_message.read
        }
        
        # Emit to both users
        room1 = f"chat_{user_id}_{data['receiver_id']}"
        room2 = f"chat_{data['receiver_id']}_{user_id}"
        emit('new_message', message_data, room=room1)
        emit('new_message', message_data, room=room2)
        
        # Generate AI response if enabled
        if data.get('ai_response', False):
            # Get conversation history
            messages = Message.query.filter(
                ((Message.sender_id == user_id) & (Message.receiver_id == data['receiver_id'])) |
                ((Message.sender_id == data['receiver_id']) & (Message.receiver_id == user_id))
            ).order_by(Message.timestamp.desc()).limit(10).all()
            
            # Format conversation for AI
            conversation = []
            for msg in reversed(messages):
                role = "user" if msg.sender_id == user_id else "assistant"
                conversation.append({"role": role, "content": msg.content})
            
            # Generate AI response
            ai_response = ai_assistant.generate_response(conversation)
            
            # Create AI message
            ai_message = Message(
                sender_id=data['receiver_id'],  # Simulating the other user
                receiver_id=user_id,
                content=ai_response,
                message_type='text',
                is_ai_generated=True
            )
            
            db.session.add(ai_message)
            db.session.commit()
            
            # Prepare AI message data
            ai_message_data = {
                'id': ai_message.id,
                'sender_id': ai_message.sender_id,
                'receiver_id': ai_message.receiver_id,
                'content': ai_message.content,
                'message_type': ai_message.message_type,
                'timestamp': ai_message.timestamp.isoformat(),
                'read': ai_message.read,
                'is_ai_generated': ai_message.is_ai_generated
            }
            
            # Emit AI response
            emit('new_message', ai_message_data, room=room1)
            emit('new_message', ai_message_data, room=room2)
            
    except Exception as e:
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])
