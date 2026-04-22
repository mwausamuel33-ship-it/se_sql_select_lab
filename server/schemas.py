"""
Marshmallow schemas for serialization, deserialization, and validation.
Handles validation at the schema level for API requests and responses.
"""
from marshmallow import Schema, fields, validates, validates_schema, ValidationError, post_load
from datetime import datetime, date


class ExerciseSchema(Schema):
    """Schema for Exercise model - basic fields."""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    category = fields.String(required=True)
    equipment_needed = fields.Boolean(required=False, load_default=False)
    created_at = fields.DateTime(dump_only=True)

    @validates('name')
    def validate_name(self, value):
        """Validate that name is not empty."""
        if not value or len(value.strip()) == 0:
            raise ValidationError('Exercise name cannot be empty')
        if len(value) > 120:
            raise ValidationError('Exercise name cannot exceed 120 characters')

    @validates('category')
    def validate_category(self, value):
        """Validate that category is not empty."""
        if not value or len(value.strip()) == 0:
            raise ValidationError('Category cannot be empty')
        if len(value) > 120:
            raise ValidationError('Category cannot exceed 120 characters')


class WorkoutExerciseNestedSchema(Schema):
    """Nested schema for WorkoutExercise within a Workout."""
    id = fields.Integer()
    exercise_id = fields.Integer()
    reps = fields.Integer(allow_none=True)
    sets = fields.Integer(allow_none=True)
    duration_seconds = fields.Integer(allow_none=True)
    exercise = fields.Nested(ExerciseSchema)


class ExerciseDetailSchema(ExerciseSchema):
    """Extended schema for Exercise with associated workouts."""
    workout_exercises = fields.Nested(
        'WorkoutExerciseNestedSchema',
        many=True,
        dump_only=True
    )


class WorkoutSchema(Schema):
    """Schema for Workout model - basic fields."""
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(required=True)
    notes = fields.String(required=False, load_default='')
    created_at = fields.DateTime(dump_only=True)

    @validates('date')
    def validate_date(self, value):
        """Validate that date is not in the future."""
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d').date()
        if value > date.today():
            raise ValidationError('Workout date cannot be in the future')

    @validates('duration_minutes')
    def validate_duration_minutes(self, value):
        """Validate that duration is positive."""
        if not isinstance(value, int) or value <= 0:
            raise ValidationError('Duration must be a positive integer')
        if value > 1440:  # More than 24 hours
            raise ValidationError('Duration cannot exceed 1440 minutes (24 hours)')


class WorkoutDetailSchema(WorkoutSchema):
    """Extended schema for Workout with associated exercises and details."""
    workout_exercises = fields.Nested(
        WorkoutExerciseNestedSchema,
        many=True,
        dump_only=True
    )


class WorkoutExerciseSchema(Schema):
    """Schema for WorkoutExercise model."""
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(required=True)
    exercise_id = fields.Integer(required=True)
    reps = fields.Integer(required=False, allow_none=True)
    sets = fields.Integer(required=False, allow_none=True)
    duration_seconds = fields.Integer(required=False, allow_none=True)
    created_at = fields.DateTime(dump_only=True)

    @validates('reps')
    def validate_reps(self, value):
        """Validate that reps is positive if provided."""
        if value is not None and value <= 0:
            raise ValidationError('Reps must be a positive integer or null')

    @validates('sets')
    def validate_sets(self, value):
        """Validate that sets is positive if provided."""
        if value is not None and value <= 0:
            raise ValidationError('Sets must be a positive integer or null')

    @validates('duration_seconds')
    def validate_duration_seconds(self, value):
        """Validate that duration_seconds is positive if provided."""
        if value is not None and value <= 0:
            raise ValidationError('Duration must be a positive integer or null')

    @validates_schema
    def validate_schema(self, data, **kwargs):
        """Validate that at least one of reps, sets, or duration_seconds is provided."""
        reps = data.get('reps')
        sets = data.get('sets')
        duration = data.get('duration_seconds')
        
        if not any([reps, sets, duration]):
            raise ValidationError(
                'At least one of reps, sets, or duration_seconds must be provided'
            )
