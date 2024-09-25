from . import db
from datetime import datetime
from flask import Blueprint, jsonify, request, session
from .models import User, Task, Reminder
import pytz
from .schemas import ReminderSchema
from .utils import send_email


reminder_schema = ReminderSchema()
reminders_schema = ReminderSchema(many=True)

# Create a Blueprint for the user routes
reminder_bp = Blueprint('reminders', __name__)

# Helper function to verify if the user exists and is logged in
def verify_user():
    user_id = session.get('user_id') # Fetch the logged-in user's ID
    if not user_id:
        return None, jsonify({'error': 'User not logged in'}), 401

    user = User.query.get(user_id)
    if not user:
        return None, jsonify({'error': 'User not found'}), 404

    return user, None, None  # Return user, response, and status code

# Helper function to fetch a reminder by ID, or return 404
def get_reminder(reminder_id, user_id):
    reminder = Reminder.query.filter_by(reminder_id=reminder_id, user_id=user_id)\
                .first_or_404(description=f'Reminder with ID {reminder_id} not found for the current user')

    return reminder

# Route for creating a new reminder
@reminder_bp.route('/reminders', methods=['POST'])
def create_reminder():
    user, error_response, status_code = verify_user() # Verify user's existence and login before action
    if error_response:
        return error_response, status_code

    data = request.json
    # Ensure a time is set for every reminder
    if 'reminder_time' not in data:
        return jsonify({'error': 'Missing reminder time'}), 400
    # Ensure every reminder is associated with a task
    task = Task.query.get(data['task_id'])
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    reminder_time = data.get('reminder_time')
    
    # Convert to datetime object
    reminder_time_obj = datetime.fromisoformat(reminder_time)
    
    # Convert to UTC if it's in another timezone
    if reminder_time_obj.tzinfo is not None:
        reminder_time_utc = reminder_time_obj.astimezone(pytz.utc)
    else:
        reminder_time_utc = reminder_time_obj  # If no timezone info, assume it's UTC

    try:
        new_reminder = Reminder(
            task_id=data['task_id'],  # Ensure a valid task ID is provided and exists
            reminder_time=reminder_time_utc,
            # The rest columns are nullable
            sent=data.get('sent', None),
            sent_time=data.get('sent_time', None)
        )

        db.session.add(new_reminder)
        db.session.commit()

        # Send an email notification
        email_subject = "New Reminder Created"
        email_body = f"Dear {User.username},\n\nYou have a new reminder set for {new_reminder.reminder_time}."
        recipient = [User.email]

        if send_email(email_subject, recipient, email_body):
            return jsonify(reminder_schema.dump(new_reminder)), 201
        else:
            return jsonify({'message': 'Reminder created, but failed to send email notification'}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create reminder', 'error': str(e)}), 500

# Route for querying all reminders for a user 
@reminder_bp.route('/reminders', methods=['GET'])
def get_all_reminders():
    user, error_response, status_code = verify_user() # Verify user's existence and login before action
    if error_response:
        return error_response, status_code

    reminders = Reminder.query.filter_by(user_id=user.id).all()
    if reminders is None:
        return jsonify({'message': 'You have no reminders'}), 200

    return jsonify(reminders_schema.dump(reminders)), 200

# Route for querying reminders by task
@reminder_bp.route('/tasks/<int:task_id>/reminders', methods=['GET'])
def get_reminders_by_task(task_id):
    user, error_response, status_code = verify_user() # Verify user's existence and login before action
    if error_response:
        return error_response, status_code

    reminders = Reminder.query.filter_by(task_id=task_id, user_id=user.id).all()
    if reminders is None:
        return jsonify({'message': 'You have no reminders for this task'}), 200

    return jsonify(reminders_schema.dump(reminders)), 200

# Route for updating a reminder
@reminder_bp.route('/reminders/<int:reminder_id>', methods=['PUT'])
def update_reminder(reminder_id):
    user, error_response, status_code = verify_user() # Verify user's existence and login before action
    if error_response:
        return error_response, status_code

    reminder = get_reminder(reminder_id, user.id)

    data = request.json

    # Handle timezone conversion for reminder_time
    if 'reminder_time' in data:
        reminder_time_obj = datetime.fromisoformat(data['reminder_time'])
        if reminder_time_obj.tzinfo is not None:
            reminder_time_utc = reminder_time_obj.astimezone(pytz.utc)
        else:
            reminder_time_utc = reminder_time_obj  # Assume UTC if no timezone info
        reminder.reminder_time = reminder_time_utc

    reminder.sent = data.get('sent', reminder.sent)
    reminder.sent_time = data.get('sent_time', reminder.sent_time)

    try:
        db.session.commit()

        # Send an email notification when the reminder is updated
        email_subject = "Reminder Updated"
        email_body = f"Dear {User.username},\n\nYour reminder has been updated to {reminder.reminder_time}."
        recipient = [User.email]

        if send_email(email_subject, recipient, email_body):
            return jsonify(reminder_schema.dump(reminder)), 200
        else:
            return jsonify({'message': 'Reminder updated, but failed to send email notification'}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update reminder', 'error': str(e)}), 500

# Route for deleting a reminder
@reminder_bp.route('/reminders/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    user, error_response, status_code = verify_user() # Verify user's existence and login before action
    if error_response:
        return error_response, status_code

    reminder = get_reminder(reminder_id, user.id)

    try:
        db.session.delete(reminder)
        db.session.commit()

        return jsonify({'message': f'Reminder with ID {reminder_id} successfully deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete reminder', 'error': str(e)}), 500
