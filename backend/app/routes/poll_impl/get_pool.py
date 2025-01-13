from flask import current_app, jsonify

def get_poll_impl(poll_id):
    try:
        if not poll_id or poll_id < 1:
            return jsonify({"error": "Invalid poll ID"}), 400
            
        poll_details = current_app.poll_service.get_poll_details(poll_id)
        if not poll_details:
            return jsonify({"error": "Poll not found"}), 404
            
        return jsonify({
            "id": poll_details["id"],
            "question": poll_details["question"],
            "options": poll_details["options"],
            "created_at": poll_details["created_at"],
            "is_active": poll_details["is_active"]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving poll: {str(e)}")
        return jsonify({"error": "Failed to retrieve poll"}), 500