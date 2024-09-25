from datetime import datetime
from marshmallow import fields, Schema, validate, validates, ValidationError


class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)  # Automatically include the user's ID
    username = fields.String(
        required=True, validate=validate.Length(min=3, max=45)
    )
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))
    notification_preference = fields.String(
        validate=validate.OneOf(['Email', 'SMS', 'Push notifications'])
    )

    @validates('password')
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError(
                "Password must be at least 8 characters long"
            )


class TaskSchema(Schema):
    task_id = fields.Int(dump_only=True)  # Automatically include the task ID
    title = fields.String(
        required=True, validate=validate.Length(min=1, max=45)
    )
    description = fields.String(required=False)
    start_time = fields.DateTime(required=False)
    end_time = fields.DateTime(required=False)
    location = fields.String(required=False)
    priority = fields.String(
        validate=validate.OneOf(['Low', 'Medium', 'High'])
    )
    status = fields.String(validate=validate.OneOf(['Pending', 'Completed']))
    recurrence = fields.String(
        validate=validate.OneOf(['None', 'Daily', 'Weekly'])
    )
    reminder_time = fields.Time(required=False)


class ReminderSchema(Schema):
    reminder_id = fields.Int(dump_only=True)  # Automatically include the reminder ID
    task_id = fields.Integer(required=True)
    reminder_time = fields.DateTime(format='%Y-%m-%dT%H:%M:%S%z', timezone='UTC', required=True) # Use UTC for timezone
    sent = fields.Boolean(default=False)
    sent_time = fields.DateTime(required=False)

    @validates('reminder_time')
    def validate_reminder_time(self, value):
        """Ensure the reminder time is not in the past and is in UTC."""
        current_time = datetime.utcnow()  # Current time in UTC
        if value < current_time:
            raise ValidationError("Reminder time cannot be in the past.")
