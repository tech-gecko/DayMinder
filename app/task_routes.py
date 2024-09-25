from flask import Blueprint, jsonify, request
from . import db
from .models import Task
from .schemas import TaskSchema


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Create a Blueprint for the user routes
task_bp = Blueprint('tasks', __name__)

# Helper function to fetch a task by ID, or return 404
def get_task(task_id):
    task = Task.query.filter_by(task_id=task_id)\
                .first_or_404(description=f'Task with ID {task_id} not found')

    return task

# Route for creating a new task
@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    # Ensure every task has a title
    if 'title' not in data:
        return jsonify({'message': 'Missing title'}), 400

    try:
        new_task = Task(
            title=data['title'],
            # The rest columns are nullable
            description=data.get('description', None),
            start_time=data.get('start_time', None),
            end_time=data.get('end_time', None),
            location=data.get('location', None),
            priority=data.get('priority', None),
            status=data.get('status', None),
            recurrence=data.get('recurrence', None),
            reminder_time=data.get('reminder_time', None)
        )

        db.session.add(new_task)
        db.session.commit()

        return jsonify(task_schema.dump(new_task)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create task', 'error': str(e)}), 500

# Route for querying a specific task by ID
@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    task = get_task(task_id)

    return jsonify(task_schema.dump(task)), 200

# Route for updating a task
@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = get_task(task_id)

    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.start_time = data.get('start_time', task.start_time)
    task.end_time = data.get('end_time', task.end_time)
    task.location = data.get('location', task.location)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    task.recurrence = data.get('recurrence', task.recurrence)
    task.reminder_time = data.get('reminder_time', task.reminder_time)

    try:
        db.session.commit()

        return jsonify(task_schema.dump(task)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update task', 'error': str(e)}), 500

# Route for deleting a task
@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = get_task(task_id)

    try:
        db.session.delete(task)
        db.session.commit()

        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete task', 'error': str(e)}), 500

# Route for querying all tasks of a user
@task_bp.route('/tasks/user/<int:user_id>', methods=['GET'])
def get_tasks_by_user(user_id):
    # Get the user's ID from the URL path and query their tasks
    tasks = Task.query.filter_by(user_id=user_id).all()

    return jsonify(tasks_schema.dump(tasks)), 200
