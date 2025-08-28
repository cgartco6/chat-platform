import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """
    Check if the file extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file, user_id):
    """
    Save an uploaded file to the server
    """
    if file and allowed_file(file.filename):
        # Create user directory if it doesn't exist
        user_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(user_dir, unique_filename)
        
        # Save file
        file.save(file_path)
        
        return file_path
    
    raise ValueError("Invalid file type")
