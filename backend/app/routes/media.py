from flask import Blueprint, request, jsonify, current_app
from app.services.media_service import MediaService

media_blueprint = Blueprint('media', __name__)

def get_media_service():
    return MediaService(current_app.config['UPLOAD_FOLDER'])

@media_blueprint.route('/upload', methods=['POST'])
def upload_media():
    media_service = get_media_service()
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    poll_id = request.form.get('poll_id')

    try:
        processed_path = media_service.process_media_file(file, poll_id)
        return jsonify({"message": "File uploaded and processed successfully", "path": processed_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@media_blueprint.route('/media/<int:poll_id>', methods=['GET'])
def get_media(poll_id):
    media_service = get_media_service()
    media_files = media_service.get_media_for_poll(poll_id)
    return jsonify({"media_files": media_files}), 200
