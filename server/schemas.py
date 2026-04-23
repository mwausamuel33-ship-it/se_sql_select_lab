from marshmallow import Schema, fields, validates, validates_schema, ValidationError
from datetime import date, datetime


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    category = fields.String(required=True)
    equipment_needed = fields.Boolean(load_default=False)
    created_at = fields.DateTime(dump_only=True)

    @validates('name')
    def validate_name(self, value):
        if not value or len(value.strip()) == 0:
            raise ValidationError('Name cannot be empty')

    @validates('category')
    def validate_category(self, value):
        if not value or len(value.strip()) == 0:
            raise ValidationError('Category cannot be empty')


# used when we want to show exercise details inside a workout response
class WorkoutExerciseNestedSchema(Schema):
    id = fields.Integer()
    exercise_id = fields.Integer()
    reps = fields.Integer(allow_none=True)
    sets = fields.Integer(allow_none=True)
    duration_seconds = fields.Integer(allow_none=True)
    exercise = fields.Nested(ExerciseSchema)


class ExerciseDetailSchema(ExerciseSchema):
    # include the workout_exercises so we can see which workouts this exercise is in
    workout_exercises = fields.Nested(WorkoutExerciseNestedSchema, many=True, dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(required=True)
    notes = fields.String(load_default='')
    created_at = fields.DateTime(dump_only=True)

    @validates('date')
    def validate_date(self, value):
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d').date()
        if value > date.today():
            raise ValidationError('Workout date cannot be in the future')

    @validates('duration_minutes')
    def validate_duration(self, value):
        if value <= 0:
            raise ValidationError('Duration must be a positive number')
        # 1440 minutes = 24 hours, no workout should be longer than that
        if value > 1440:
            raise ValidationError('Duration cannot exceed 1440 minutes (24 hours)')


class WorkoutDetailSchema(WorkoutSchema):
    # include exercises with their reps/sets/duration info
    workout_exercises = fields.Nested(WorkoutExerciseNestedSchema, many=True, dump_only=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(dump_only=True)
    exercise_id = fields.Integer(dump_only=True)
    reps = fields.Integer(allow_none=True)
    sets = fields.Integer(allow_none=True)
    duration_seconds = fields.Integer(allow_none=True)
    created_at = fields.DateTime(dump_only=True)

    @validates('reps')
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError('Reps must be a positive number')

    @validates('sets')
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError('Sets must be a positive number')

    @validates('duration_seconds')
    def validate_duration_seconds(self, value):
        if value is not None and value <= 0:
            raise ValidationError('Duration must be a positive number')

    @validates_schema
    def validate_has_data(self, data, **kwargs):
        # need at least one of these to be provided
        if not any([data.get('reps'), data.get('sets'), data.get('duration_seconds')]):
            raise ValidationError('Must provide at least one of: reps, sets, or duration_seconds')
