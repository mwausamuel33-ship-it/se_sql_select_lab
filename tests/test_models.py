"""
Tests for database models: Exercise, Workout, and WorkoutExercise.
"""
import pytest
import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from app import app, db
from models import Exercise, Workout, WorkoutExercise


class TestExerciseModel:
    """Test the Exercise model."""

    def test_create_exercise(self, app_client):
        """Test creating an exercise."""
        with app.app_context():
            exercise = Exercise(
                name='Pull-ups',
                category='Upper Body',
                equipment_needed=False
            )
            db.session.add(exercise)
            db.session.commit()
            
            assert exercise.id is not None
            assert exercise.name == 'Pull-ups'
            assert exercise.category == 'Upper Body'
            assert exercise.equipment_needed is False

    def test_exercise_name_required(self, app_client):
        """Test that exercise name is required and cannot be empty."""
        with app.app_context():
            with pytest.raises(ValueError):
                exercise = Exercise(
                    name='',
                    category='Upper Body',
                    equipment_needed=False
                )

    def test_exercise_category_required(self, app_client):
        """Test that exercise category is required."""
        with app.app_context():
            with pytest.raises(ValueError):
                exercise = Exercise(
                    name='Pull-ups',
                    category='',
                    equipment_needed=False
                )

    def test_exercise_name_whitespace_only(self, app_client):
        """Test that exercise name cannot be only whitespace."""
        with app.app_context():
            with pytest.raises(ValueError):
                exercise = Exercise(
                    name='   ',
                    category='Upper Body',
                    equipment_needed=False
                )

    def test_exercise_unique_constraint(self, app_client):
        """Test that combination of name and category must be unique."""
        with app.app_context():
            exercise1 = Exercise(
                name='Pull-ups',
                category='Upper Body',
                equipment_needed=False
            )
            db.session.add(exercise1)
            db.session.commit()
            
            exercise2 = Exercise(
                name='Pull-ups',
                category='Upper Body',
                equipment_needed=True
            )
            db.session.add(exercise2)
            
            with pytest.raises(Exception):  # IntegrityError
                db.session.commit()


class TestWorkoutModel:
    """Test the Workout model."""

    def test_create_workout(self, app_client):
        """Test creating a workout."""
        with app.app_context():
            today = date.today()
            workout = Workout(
                date=today - timedelta(days=1),
                duration_minutes=60,
                notes='Good session'
            )
            db.session.add(workout)
            db.session.commit()
            
            assert workout.id is not None
            assert workout.duration_minutes == 60
            assert workout.notes == 'Good session'

    def test_workout_duration_positive(self, app_client):
        """Test that workout duration must be positive."""
        with app.app_context():
            today = date.today()
            with pytest.raises(ValueError):
                workout = Workout(
                    date=today,
                    duration_minutes=-10,
                    notes='Invalid'
                )

    def test_workout_duration_zero(self, app_client):
        """Test that workout duration cannot be zero."""
        with app.app_context():
            today = date.today()
            with pytest.raises(ValueError):
                workout = Workout(
                    date=today,
                    duration_minutes=0,
                    notes='Invalid'
                )

    def test_workout_date_not_future(self, app_client):
        """Test that workout date cannot be in the future."""
        with app.app_context():
            tomorrow = date.today() + timedelta(days=1)
            with pytest.raises(ValueError):
                workout = Workout(
                    date=tomorrow,
                    duration_minutes=60,
                    notes='Future date'
                )

    def test_workout_date_today_allowed(self, app_client):
        """Test that today's date is allowed for workout."""
        with app.app_context():
            today = date.today()
            workout = Workout(
                date=today,
                duration_minutes=60,
                notes='Today'
            )
            db.session.add(workout)
            db.session.commit()
            
            assert workout.id is not None


class TestWorkoutExerciseModel:
    """Test the WorkoutExercise model."""

    def test_create_workout_exercise_with_reps_sets(self, app_client, sample_exercises, sample_workouts):
        """Test creating a workout exercise with reps and sets."""
        with app.app_context():
            we = WorkoutExercise(
                workout_id=1,
                exercise_id=1,
                reps=10,
                sets=3,
                duration_seconds=None
            )
            db.session.add(we)
            db.session.commit()
            
            assert we.id is not None
            assert we.reps == 10
            assert we.sets == 3

    def test_create_workout_exercise_with_duration(self, app_client, sample_exercises, sample_workouts):
        """Test creating a workout exercise with duration."""
        with app.app_context():
            we = WorkoutExercise(
                workout_id=1,
                exercise_id=1,
                reps=None,
                sets=None,
                duration_seconds=1800
            )
            db.session.add(we)
            db.session.commit()
            
            assert we.id is not None
            assert we.duration_seconds == 1800

    def test_workout_exercise_requires_at_least_one_metric(self, app_client, sample_exercises, sample_workouts):
        """Test that workout exercise must have at least one metric."""
        with app.app_context():
            we = WorkoutExercise(
                workout_id=1,
                exercise_id=1,
                reps=None,
                sets=None,
                duration_seconds=None
            )
            db.session.add(we)
            
            with pytest.raises(Exception):  # CheckConstraint violation
                db.session.commit()

    def test_workout_exercise_reps_positive(self, app_client, sample_exercises, sample_workouts):
        """Test that reps must be positive if provided."""
        with app.app_context():
            with pytest.raises(ValueError):
                we = WorkoutExercise(
                    workout_id=1,
                    exercise_id=1,
                    reps=-5,
                    sets=3,
                    duration_seconds=None
                )

    def test_workout_exercise_sets_positive(self, app_client, sample_exercises, sample_workouts):
        """Test that sets must be positive if provided."""
        with app.app_context():
            with pytest.raises(ValueError):
                we = WorkoutExercise(
                    workout_id=1,
                    exercise_id=1,
                    reps=10,
                    sets=0,
                    duration_seconds=None
                )

    def test_workout_exercise_duration_positive(self, app_client, sample_exercises, sample_workouts):
        """Test that duration_seconds must be positive if provided."""
        with app.app_context():
            with pytest.raises(ValueError):
                we = WorkoutExercise(
                    workout_id=1,
                    exercise_id=1,
                    reps=None,
                    sets=None,
                    duration_seconds=-100
                )

    def test_workout_exercise_cascade_delete(self, app_client, sample_exercises, sample_workouts, sample_workout_exercises):
        """Test that deleting a workout cascades to workout_exercises."""
        with app.app_context():
            assert WorkoutExercise.query.count() == 2
            
            workout = Workout.query.get(1)
            db.session.delete(workout)
            db.session.commit()
            
            assert Workout.query.count() == 1
            assert WorkoutExercise.query.count() == 1
