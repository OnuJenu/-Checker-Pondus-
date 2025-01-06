"""
Media Model

This model handles the media files associated with polls within the mobile voting platform. It manages the storage and retrieval of various media types, ensuring that each poll can include rich media content. The Media model is essential for enhancing user engagement and supporting diverse content formats, including:

Attributes:
- id: A unique identifier for each media file, serving as the primary key.
- poll_id: An integer referencing the poll to which the media is associated, linked to the Poll model.
- media_type: A string indicating the type of media (e.g., 'image', 'video', 'audio').
- file_path: A string representing the file path where the media is stored.

Methods:
- upload_media: A method to handle the logic for uploading new media files to the system.
- get_media_by_poll: A method to retrieve all media files associated with a specific poll ID.

The Media model ensures that each media file is correctly linked to its corresponding poll and stored efficiently. This model is designed to integrate with the media handling system, supporting the secure and scalable management of media content.
"""
import os
from werkzeug.utils import secure_filename
from flask import request, current_app
from app import db

def allowed_file(filename):
    """
    Checks if a file has an allowed extension.
    
    Args:
        filename (str): The name of the file to check.
        
    Returns:
        bool: True if the file is allowed, False otherwise.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    media_type = db.Column(db.String(50), nullable=False)  # e.g., 'image', 'video', 'audio'
    file_path = db.Column(db.String(255), nullable=False)

    def upload_media(self, poll_id, uploaded_file):
        """
        Uploads a media file and stores its path in the database.

        Args:
            poll_id (int): The ID of the poll to which the media belongs.
            uploaded_file: The file object from the request.

        Returns:
            bool: True if the upload was successful, False otherwise.
        """
        # Check if the file part is present
        if 'file' not in request.files:
            return False

        file = request.files['file']

        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            return False

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Define the path to save the file
            base_path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(poll_id))
            if not os.path.exists(base_path):
                os.makedirs(base_path)
                
            full_path = os.path.join(base_path, filename)
            file.save(full_path)

            # Create a new Media entry in the database
            media_entry = Media(
                poll_id=poll_id,
                media_type=file.content_type.split('/')[0],  # Determine type based on MIME type
                file_path=full_path
            )
            db.session.add(media_entry)
            db.session.commit()
            
            return True

        return False

    @classmethod
    def get_media_by_poll(cls, poll_id):
        """
        Retrieves all media files associated with a specific poll ID.
        
        Args:
            poll_id (int): The ID of the poll for which to retrieve media.
            
        Returns:
            list: A list of Media objects associated with the given poll ID.
        """
        return cls.query.filter_by(poll_id=poll_id).all()