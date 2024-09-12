from app import db


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45), unique=True, nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)
    notification_preference = db.Column(
        db.Enum('Email', 'SMS', 'Push notifications')
    )

    # Relationship to 'tasks'
    tasks = db.relationship(
        'Task', back_populates='user', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<User(user_id='{self.user_id}', username='{self.username}')>"


class Task(db.Model):
    __tablename__ = 'tasks'
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id'), nullable=False
    )
    title = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    location = db.Column(db.String(45))
    priority = db.Column(db.Enum('Low', 'Medium', 'High'))
    status = db.Column(db.Enum('Pending', 'Completed'))
    recurrence = db.Column(db.Enum('None', 'Daily', 'Weekly'))
    reminder_time = db.Column(db.TIMESTAMP)

    # Relationship to 'users'
    user = db.relationship('User', back_populates='tasks')

    # Relationship to 'reminders'
    reminders = db.relationship(
        'Reminder', back_populates='task', cascade='all, delete-orphan'
        )

    def __repr__(self):
        return (
            f"<Task(task_id='{self.task_id}', user_id='{self.user_id}', "
            f"title='{self.title}')>"
        )


class Reminder(db.Model):
    __tablename__ = 'reminders'
    reminder_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(
        db.Integer, db.ForeignKey('tasks.task_id'), nullable=False
    )
    reminder_time = db.Column(db.TIMESTAMP, nullable=False)
    sent = db.Column(db.Boolean, default=False)
    sent_time = db.Column(db.DateTime, nullable=True)

    # Relationship to 'tasks'
    task = db.relationship('Task', back_populates='reminders')

    def __repr__(self):
        return (
            f"<Reminder(reminder_id='{self.reminder_id}', "
            f"task_id='{self.task_id}', "
            f"reminder_time='{self.reminder_time}', sent='{self.sent}')>"
        )
