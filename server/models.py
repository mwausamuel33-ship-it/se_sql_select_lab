"""
Database models for the workout tracking application.
Defines Exercise, Workout, and WorkoutExercise models with validations and relationships.
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, UniqueConstraint
from datetime import datetime

db = SQLAlchemy()


class Exercise(db.Model):
    """
    Represents an exercise that can be added to workouts.
    """
    __tablename__ = 'exercises'

    # Table constraints
    __table_args__ = (
        UniqueConstraint('name', 'category', name='uq_exercise_name_category'),
        CheckConstraint('length(name) > 0', name='ck_exercise_name_not_empty'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='exercise',
        cascade='all, delete-orphan'
    )
    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        back_populates='exercises',
        viewonly=True
    )

    @validates('name')
    def validate_name(self, key, value):
        """Validate that name is not empty and is a string."""
        if not value or not isinstance(value, str):
            raise ValueError('Exercise name must be a non-empty string')
        if len(value.strip()) == 0:
            raise ValueError('Exercise name cannot be only whitespace')
        return value.strip()

    @validates('category')
    def validate_category(self, key, value):
        """Validate that category is not empty and is a string."""
        if not value or not isinstance(value, str):
            raise ValueError('Category must be a non-empty string')
        if len(value.strip()) == 0:
            raise ValueError('Category cannot be only whitespace')
        return value.strip()

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


class Workout(db.Model):
    """
    Represents a workout session with associated exercises.
    """
    __tablename__ = 'workouts'

    # Table constraints
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='ck_workout_duration_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan'
    )
    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        back_populates='workouts',
        viewonly=True
    )

    @validates('duration_minutes')
    def validate_duration_minutes(self, key, value):
        """Validate that duration is a positive integer."""
        if not isinstance(value, int):
            raise ValueError('Duration must be an integer')
        if value <= 0:
            raise ValueError('Duration must be greater than 0')
        return value

    @validates('date')
    def validate_date(self, key, value):
        """Validate that date is not in the future."""
        from datetime import date
        if isinstance(value, str):
            from datetime import datetime as dt
            value = dt.strptime(value, '%Y-%m-%d').date()
        if value > date.today():
            raise ValueError('Workout date cannot be in the future')
        return value

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'


class WorkoutExercise(db.Model):
    """
    Join table representing an exercise within a workout.
    Tracks reps, sets, and duration for each exercise in a workout.
    """
    __tablename__ = 'workout_exercises'

    # Table constraints
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

    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps')
    def validate_reps(self, key, value):
        """Validate that reps is positive if provided."""
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError('Reps must be a positive integer or None')
        return value

    @validates('sets')
    def validate_sets(self, key, value):
        """Validate that sets is positive if provided."""
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError('Sets must be a positive integer or None')
        return value

    @validates('duration_seconds')
    def validate_duration_seconds(self, key, value):
        """Validate that duration_seconds is positive if provided."""
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError('Duration must be a positive integer or None')
        return value

    def __repr__(self):
        return f'<WorkoutExercise {self.id}: Workout {self.workout_id}, Exercise {self.exercise_id}>'
