"""
Pytest configuration and fixtures for the Workout Tracking API tests.
"""
import pytest
import sys
import os

# Add server directory to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from app import app, db
from models import Exercise, Workout, WorkoutExercise
from datetime import date, timedelta


@pytest.fixture
def app_client():
    """Create a Flask test client with a temporary test database."""
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    # Create instance directory if it doesn't exist
    os.makedirs('instance', exist_ok=True)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        yield app.test_client()
        # Clean up after tests
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_exercises(app_client):
    """Create sample exercise data for testing."""
    with app.app_context():
        exercises = [
            Exercise(
                name='Barbell Squat',
                category='Lower Body',
                equipment_needed=True
            ),
            Exercise(
                name='Bench Press',
                category='Upper Body',
                equipment_needed=True
            ),
            Exercise(
                name='Running',
                category='Cardio',
                equipment_needed=False
            ),
        ]
        for exercise in exercises:
            db.session.add(exercise)
        db.session.commit()
        return exercises


@pytest.fixture
def sample_workouts(app_client):
    """Create sample workout data for testing."""
    with app.app_context():
        today = date.today()
        workouts = [
            Workout(
                date=today - timedelta(days=2),
                duration_minutes=60,
                notes='Upper body day'
            ),
            Workout(
                date=today - timedelta(days=1),
                duration_minutes=45,
                notes='Cardio session'
            ),
        ]
        for workout in workouts:
            db.session.add(workout)
        db.session.commit()
        return workouts


@pytest.fixture
def sample_workout_exercises(app_client, sample_exercises, sample_workouts):
    """Create sample workout exercise associations for testing."""
    with app.app_context():
        workout_exercises = [
            WorkoutExercise(
                workout_id=1,
                exercise_id=1,
                reps=5,
                sets=5,
                duration_seconds=None
            ),
            WorkoutExercise(
                workout_id=2,
                exercise_id=3,
                reps=None,
                sets=None,
                duration_seconds=1800  # 30 minutes
            ),
        ]
        for we in workout_exercises:
            db.session.add(we)
        db.session.commit()
        return workout_exercises
