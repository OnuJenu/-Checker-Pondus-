from flask import request, Blueprint
from app.routes.poll_impl.create_poll import create_poll_impl
from app.routes.poll_impl.get_polls import get_polls_impl
from app.routes.poll_impl.get_poll import get_poll_impl
from app.routes.poll_impl.poll_vote import poll_vote_impl
from app.routes.poll_impl.get_poll_results import get_poll_results_impl

poll_blueprint = Blueprint('poll', __name__)

# Provides a paginated list of polls.
# Supports filtering by active or closed polls.
# Returns a list of polls with basic details and pagination information.
# Retrieve a paginated list of polls
@poll_blueprint.route('/polls', methods=['GET'])
def get_polls():
    return get_polls_impl(request)

# Handles the creation of a new poll.
# Validates and saves media if provided.
# Ensures that each poll has exactly two options.
@poll_blueprint.route('/polls', methods=['POST'])
def create_poll():
    return create_poll_impl(request)

# Retrieves a specific poll by its ID.
# Returns details including the question, media URL, options, and creation date.
# Retrieve specific poll
@poll_blueprint.route('/polls/<int:poll_id>', methods=['GET'])
def get_poll(poll_id):
    return get_poll_impl(poll_id)

# Allows users to vote on a poll.
# Ensures that the user has not already voted and that the poll is not closed.
# Records the vote in the database.
# Vote on a poll
@poll_blueprint.route('/polls/<int:poll_id>/vote', methods=['POST'])
def vote(poll_id):
    return poll_vote_impl(poll_id, request)


# Retrieves the results of a closed poll.
# Calculates the percentage of votes for each option.
# Returns the results in a user-friendly format.
# Get closed poll results
@poll_blueprint.route('/polls/<int:poll_id>/results', methods=['GET'])
def get_poll_results(poll_id):
    return get_poll_results_impl(poll_id)

# # Allows the creator of a poll to close it, preventing further voting.
# # Ensures that only the creator can close the poll.
# # Close a poll
# @poll_blueprint.route('/polls/<int:poll_id>/close', methods=['PUT'])
# def close_poll(poll_id):
#     user = get_current_user()
#     poll = Poll.query.get_or_404(poll_id)

#     if poll.user_id != user.id:
#         return jsonify({"error": "You are not authorized to close this poll"}), 403

#     poll.closed = True
#     db.session.commit()

#     return jsonify({"message": "Poll closed"}), 200
