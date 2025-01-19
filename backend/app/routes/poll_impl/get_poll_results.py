from flask import current_app, jsonify

from app.models.poll import Poll


def get_poll_results_impl(poll_id):
    try:
        if not poll_id or poll_id < 1:
            return jsonify({"error": "Invalid poll ID"}), 400
            
        poll = Poll.get_poll_by_id(poll_id)
        if poll.is_active:
            return jsonify({"error": "Poll results are not available yet"}), 403

        options = [
            {
                "id": option.id,
                "text": option.description,
                "vote_count": len(poll.get_votes_for_option(option.id))
            }
            for option in poll.voting_options
        ]

        total_votes = sum([option['vote_count'] for option in options])
        results = [
            {**option, "percentage": (option["vote_count"] / total_votes) * 100 if total_votes > 0 else 0}
            for option in options
        ]

        return jsonify({
            "id": poll.id,
            "question": poll.question,
            "results": results,
            "total_votes": total_votes
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error retrieving poll: {str(e)}")
        return jsonify({"error": "Failed to retrieve poll"}), 500