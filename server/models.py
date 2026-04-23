from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, UniqueConstraint
from datetime import date, datetime

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'

    # make sure name+category combo is unique and name can't be empty
    __table_args__ = (
        UniqueConstraint('name', 'category', name='uq_exercise_name_category'),
        CheckConstraint('length(name) > 0', name='ck_exercise_name_not_empty'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises', viewonly=True)

    @validates('name')
    def validate_name(self, key, value):
        if not value or not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError('Exercise name must be a non-empty string')
        return value.strip()

    @validates('category')
    def validate_category(self, key, value):
        if not value or not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError('Category must be a non-empty string')
        return value.strip()

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    # duration has to be a positive number
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='ck_workout_duration_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts', viewonly=True)

    @validates('date')
    def validate_date(self, key, value):
        # convert string to date if needed
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d').date()
        if value > date.today():
            raise ValueError('Workout date cannot be in the future')
        return value

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError('Duration must be a positive integer')
        return value

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    # at least one of reps, sets, or duration_seconds must be provided
    __table_args__ = (
        CheckConstraint('reps > 0 OR sets > 0 OR duration_seconds > 0', name='ck_workout_exercise_has_data'),
        CheckConstraint('reps IS NULL OR reps > 0', name='ck_workout_exercise_reps_positive'),
        CheckConstraint('sets IS NULL OR sets > 0', name='ck_workout_exercise_sets_positive'),
        CheckConstraint('duration_seconds IS NULL OR duration_seconds > 0', name='ck_workout_exercise_duration_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps')
    def validate_reps(self, key, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError('Reps must be a positive integer')
        return value

    @validates('sets')
    def validate_sets(self, key, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError('Sets must be a positive integer')
        return value

    @validates('duration_seconds')
    def validate_duration_seconds(self, key, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError('Duration seconds must be a positive integer')
        return value

    def __repr__(self):
        return f'<WorkoutExercise workout={self.workout_id} exercise={self.exercise_id}>'
