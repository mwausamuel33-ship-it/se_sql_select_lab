"""
Tests for Flask API endpoints.
"""
import pytest
import sys
import os
import json
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from app import app, db
from models import Exercise, Workout, WorkoutExercise


class TestExerciseEndpoints:
    """Test Exercise endpoints."""

    def test_get_exercises(self, app_client, sample_exercises):
        """Test GET /exercises."""
        response = app_client.get('/exercises')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 3
        assert data[0]['name'] == 'Barbell Squat'

    def test_get_exercise_by_id(self, app_client, sample_exercises):
        """Test GET /exercises/<id>."""
        response = app_client.get('/exercises/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == 1
        assert data['name'] == 'Barbell Squat'
        assert data['category'] == 'Lower Body'

    def test_get_exercise_not_found(self, app_client):
        """Test GET /exercises/<id> with non-existent id."""
        response = app_client.get('/exercises/999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_create_exercise_valid(self, app_client):
        """Test POST /exercises with valid data."""
        payload = {
            'name': 'Deadlift',
            'category': 'Full Body',
            'equipment_needed': True
        }
        response = app_client.post(
            '/exercises',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Deadlift'
        assert data['category'] == 'Full Body'

    def test_create_exercise_missing_name(self, app_client):
        """Test POST /exercises with missing name."""
        payload = {
            'category': 'Full Body',
            'equipment_needed': True
        }
        response = app_client.post(
            '/exercises',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_create_exercise_empty_name(self, app_client):
        """Test POST /exercises with empty name."""
        payload = {
            'name': '',
            'category': 'Full Body',
            'equipment_needed': True
        }
        response = app_client.post(
            '/exercises',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_create_exercise_missing_category(self, app_client):
        """Test POST /exercises with missing category."""
        payload = {
            'name': 'Deadlift',
            'equipment_needed': True
        }
        response = app_client.post(
            '/exercises',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_delete_exercise(self, app_client, sample_exercises):
        """Test DELETE /exercises/<id>."""
        with app.app_context():
            assert Exercise.query.count() == 3
        
        response = app_client.delete('/exercises/1')
        assert response.status_code == 204
        
        with app.app_context():
            assert Exercise.query.count() == 2

    def test_delete_exercise_not_found(self, app_client):
        """Test DELETE /exercises/<id> with non-existent id."""
        response = app_client.delete('/exercises/999')
        assert response.status_code == 404


class TestWorkoutEndpoints:
    """Test Workout endpoints."""

    def test_get_workouts(self, app_client, sample_workouts):
        """Test GET /workouts."""
        response = app_client.get('/workouts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['duration_minutes'] == 60

    def test_get_workout_by_id(self, app_client, sample_workouts):
        """Test GET /workouts/<id>."""
        response = app_client.get('/workouts/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == 1
        assert data['duration_minutes'] == 60

    def test_get_workout_not_found(self, app_client):
        """Test GET /workouts/<id> with non-existent id."""
        response = app_client.get('/workouts/999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_create_workout_valid(self, app_client):
        """Test POST /workouts with valid data."""
        today = str(date.today())
        payload = {
            'date': today,
            'duration_minutes': 45,
            'notes': 'Cardio session'
        }
        response = app_client.post(
            '/workouts',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['duration_minutes'] == 45
        assert data['notes'] == 'Cardio session'

    def test_create_workout_missing_date(self, app_client):
        """Test POST /workouts with missing date."""
        payload = {
            'duration_minutes': 45,
            'notes': 'Cardio session'
        }
        response = app_client.post(
            '/workouts',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code in [400, 422]  # 400 or 422 for missing required field

    def test_create_workout_future_date(self, app_client):
        """Test POST /workouts with future date."""
        tomorrow = str(date.today() + timedelta(days=1))
        payload = {
            'date': tomorrow,
            'duration_minutes': 45,
            'notes': 'Future workout'
        }
        response = app_client.post(
            '/workouts',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_create_workout_invalid_duration(self, app_client):
        """Test POST /workouts with invalid duration."""
        today = str(date.today())
        payload = {
            'date': today,
            'duration_minutes': 0,
            'notes': 'Invalid'
        }
        response = app_client.post(
            '/workouts',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_delete_workout(self, app_client, sample_workouts):
        """Test DELETE /workouts/<id>."""
        with app.app_context():
            assert Workout.query.count() == 2
        
        response = app_client.delete('/workouts/1')
        assert response.status_code == 204
        
        with app.app_context():
            assert Workout.query.count() == 1

    def test_delete_workout_not_found(self, app_client):
        """Test DELETE /workouts/<id> with non-existent id."""
        response = app_client.delete('/workouts/999')
        assert response.status_code == 404


class TestWorkoutExerciseEndpoints:
    """Test WorkoutExercise endpoints."""

    def test_add_exercise_to_workout(self, app_client, sample_exercises, sample_workouts):
        """Test POST /workouts/<id>/exercises/<id>/workout_exercises."""
        payload = {
            'reps': 10,
            'sets': 4,
            'duration_seconds': None
        }
        response = app_client.post(
            '/workouts/1/exercises/1/workout_exercises',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['workout_id'] == 1
        assert data['exercise_id'] == 1
        assert data['reps'] == 10

    def test_add_exercise_with_duration(self, app_client, sample_exercises, sample_workouts):
        """Test adding exercise with duration instead of reps/sets."""
        payload = {
            'reps': None,
            'sets': None,
            'duration_seconds': 1800
        }
        response = app_client.post(
            '/workouts/1/exercises/2/workout_exercises',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['duration_seconds'] == 1800

    def test_add_exercise_workout_not_found(self, app_client, sample_exercises):
        """Test adding exercise to non-existent workout."""
        payload = {
            'reps': 10,
            'sets': 4,
            'duration_seconds': None
        }
        response = app_client.post(
            '/workouts/999/exercises/1/workout_exercises',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'Workout not found' in data['error']

    def test_add_exercise_not_found(self, app_client, sample_workouts):
        """Test adding non-existent exercise to workout."""
        payload = {
            'reps': 10,
            'sets': 4,
            'duration_seconds': None
        }
        response = app_client.post(
            '/workouts/1/exercises/999/workout_exercises',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'Exercise not found' in data['error']

    def test_add_exercise_no_metrics(self, app_client, sample_exercises, sample_workouts):
        """Test adding exercise without any metrics."""
        payload = {
            'reps': None,
            'sets': None,
            'duration_seconds': None
        }
        response = app_client.post(
            '/workouts/1/exercises/1/workout_exercises',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'At least one' in str(data)

    def test_add_duplicate_exercise_to_workout(self, app_client, sample_exercises, sample_workouts, sample_workout_exercises):
        """Test adding the same exercise twice to a workout."""
        payload = {
            'reps': 12,
            'sets': 3,
            'duration_seconds': None
        }
        response = app_client.post(
            '/workouts/1/exercises/1/workout_exercises',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'already in this workout' in data['error']


class TestErrorHandling:
    """Test error handling."""

    def test_404_not_found(self, app_client):
        """Test 404 error handling."""
        response = app_client.get('/nonexistent')
        assert response.status_code == 404

    def test_get_empty_exercises_list(self, app_client):
        """Test getting exercises when database is empty."""
        response = app_client.get('/exercises')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_get_empty_workouts_list(self, app_client):
        """Test getting workouts when database is empty."""
        response = app_client.get('/workouts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []
