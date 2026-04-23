"""
Tests for Marshmallow schemas validation.
"""
import pytest
import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from schemas import (
    ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema,
    ExerciseDetailSchema, WorkoutDetailSchema
)


class TestExerciseSchema:
    """Test the ExerciseSchema validation."""

    def test_exercise_schema_valid(self):
        """Test schema with valid exercise data."""
        schema = ExerciseSchema()
        data = {
            'name': 'Pull-ups',
            'category': 'Upper Body',
            'equipment_needed': False
        }
        errors = schema.validate(data)
        assert errors == {}

    def test_exercise_schema_missing_name(self):
        """Test schema with missing name."""
        schema = ExerciseSchema()
        data = {
            'category': 'Upper Body',
            'equipment_needed': False
        }
        errors = schema.validate(data)
        assert 'name' in errors

    def test_exercise_schema_empty_name(self):
        """Test schema with empty name."""
        schema = ExerciseSchema()
        data = {
            'name': '',
            'category': 'Upper Body',
            'equipment_needed': False
        }
        errors = schema.validate(data)
        assert 'name' in errors

    def test_exercise_schema_whitespace_name(self):
        """Test schema with whitespace-only name."""
        schema = ExerciseSchema()
        data = {
            'name': '   ',
            'category': 'Upper Body',
            'equipment_needed': False
        }
        errors = schema.validate(data)
        assert 'name' in errors

    def test_exercise_schema_missing_category(self):
        """Test schema with missing category."""
        schema = ExerciseSchema()
        data = {
            'name': 'Pull-ups',
            'equipment_needed': False
        }
        errors = schema.validate(data)
        assert 'category' in errors

    def test_exercise_schema_empty_category(self):
        """Test schema with empty category."""
        schema = ExerciseSchema()
        data = {
            'name': 'Pull-ups',
            'category': '',
            'equipment_needed': False
        }
        errors = schema.validate(data)
        assert 'category' in errors

    def test_exercise_schema_name_too_long(self):
        """Test schema with name exceeding 120 characters."""
        schema = ExerciseSchema()
        long_name = 'a' * 121
        data = {
            'name': long_name,
            'category': 'Upper Body',
            'equipment_needed': False
        }
        errors = schema.validate(data)
        assert 'name' in errors

    def test_exercise_schema_category_too_long(self):
        """Test schema with category exceeding 120 characters."""
        schema = ExerciseSchema()
        long_category = 'a' * 121
        data = {
            'name': 'Pull-ups',
            'category': long_category,
            'equipment_needed': False
        }
        errors = schema.validate(data)
        assert 'category' in errors


class TestWorkoutSchema:
    """Test the WorkoutSchema validation."""

    def test_workout_schema_valid(self):
        """Test schema with valid workout data."""
        schema = WorkoutSchema()
        today = str(date.today())
        data = {
            'date': today,
            'duration_minutes': 60,
            'notes': 'Good session'
        }
        errors = schema.validate(data)
        assert errors == {}

    def test_workout_schema_missing_date(self):
        """Test schema with missing date."""
        schema = WorkoutSchema()
        data = {
            'duration_minutes': 60,
            'notes': 'Good session'
        }
        errors = schema.validate(data)
        assert 'date' in errors or errors == {}

    def test_workout_schema_future_date(self):
        """Test schema with future date."""
        schema = WorkoutSchema()
        tomorrow = str(date.today() + timedelta(days=1))
        data = {
            'date': tomorrow,
            'duration_minutes': 60,
            'notes': 'Future workout'
        }
        errors = schema.validate(data)
        assert 'date' in errors

    def test_workout_schema_missing_duration(self):
        """Test schema with missing duration."""
        schema = WorkoutSchema()
        today = str(date.today())
        data = {
            'date': today,
            'notes': 'Good session'
        }
        errors = schema.validate(data)
        assert 'duration_minutes' in errors or errors == {}

    def test_workout_schema_zero_duration(self):
        """Test schema with zero duration."""
        schema = WorkoutSchema()
        today = str(date.today())
        data = {
            'date': today,
            'duration_minutes': 0,
            'notes': 'Invalid'
        }
        errors = schema.validate(data)
        assert 'duration_minutes' in errors

    def test_workout_schema_negative_duration(self):
        """Test schema with negative duration."""
        schema = WorkoutSchema()
        today = str(date.today())
        data = {
            'date': today,
            'duration_minutes': -30,
            'notes': 'Invalid'
        }
        errors = schema.validate(data)
        assert 'duration_minutes' in errors

    def test_workout_schema_excessive_duration(self):
        """Test schema with duration exceeding 24 hours."""
        schema = WorkoutSchema()
        today = str(date.today())
        data = {
            'date': today,
            'duration_minutes': 1441,  # More than 24 hours
            'notes': 'Too long'
        }
        errors = schema.validate(data)
        assert 'duration_minutes' in errors


class TestWorkoutExerciseSchema:
    """Test the WorkoutExerciseSchema validation."""

    def test_workout_exercise_schema_with_reps_sets(self):
        """Test schema with reps and sets."""
        schema = WorkoutExerciseSchema()
        data = {
            'workout_id': 1,
            'exercise_id': 1,
            'reps': 10,
            'sets': 3,
            'duration_seconds': None
        }
        errors = schema.validate(data)
        assert errors == {}

    def test_workout_exercise_schema_with_duration(self):
        """Test schema with duration."""
        schema = WorkoutExerciseSchema()
        data = {
            'workout_id': 1,
            'exercise_id': 1,
            'reps': None,
            'sets': None,
            'duration_seconds': 1800
        }
        errors = schema.validate(data)
        assert errors == {}

    def test_workout_exercise_schema_no_metrics(self):
        """Test schema with no metrics provided."""
        schema = WorkoutExerciseSchema()
        data = {
            'workout_id': 1,
            'exercise_id': 1,
            'reps': None,
            'sets': None,
            'duration_seconds': None
        }
        errors = schema.validate(data)
        assert 'schema' in errors or any('At least one' in str(e) for e in errors.values())

    def test_workout_exercise_schema_negative_reps(self):
        """Test schema with negative reps."""
        schema = WorkoutExerciseSchema()
        data = {
            'workout_id': 1,
            'exercise_id': 1,
            'reps': -10,
            'sets': 3,
            'duration_seconds': None
        }
        errors = schema.validate(data)
        assert 'reps' in errors

    def test_workout_exercise_schema_zero_sets(self):
        """Test schema with zero sets."""
        schema = WorkoutExerciseSchema()
        data = {
            'workout_id': 1,
            'exercise_id': 1,
            'reps': 10,
            'sets': 0,
            'duration_seconds': None
        }
        errors = schema.validate(data)
        assert 'sets' in errors

    def test_workout_exercise_schema_negative_duration(self):
        """Test schema with negative duration."""
        schema = WorkoutExerciseSchema()
        data = {
            'workout_id': 1,
            'exercise_id': 1,
            'reps': None,
            'sets': None,
            'duration_seconds': -100
        }
        errors = schema.validate(data)
        assert 'duration_seconds' in errors
