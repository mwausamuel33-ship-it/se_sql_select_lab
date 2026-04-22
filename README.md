# Workout Tracking API

A Flask-based backend API for tracking workouts and exercises. Personal trainers use this API to manage their clients' workout data, including exercises with sets, reps, and duration information.

## Features

- CRUD operations for Exercises and Workouts
- Add exercises to workouts with sets/reps/duration tracking
- Validations at model and schema levels
- Database constraints for data integrity
- Marshmallow schemas for serialization/deserialization

## Installation

```bash
# Install dependencies
pipenv install

# Run migrations
cd server
PYTHONPATH=. FLASK_APP=app.py flask db upgrade

# Seed the database
cd ..
PYTHONPATH=server python3 -c "import server.seed; server.seed.seed_database()"
```

## Running the API

```bash
cd server
PYTHONPATH=. FLASK_APP=app.py flask run --port=5555
```

Or run the app directly:

```bash
cd server
PYTHONPATH=. python3 app.py
```

## API Endpoints

### Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get exercise with associated workouts |
| POST | `/exercises` | Create a new exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Get workout with exercises and sets/reps/duration |
| POST | `/workouts` | Create a new workout |
| DELETE | `/workouts/<id>` | Delete a workout |

### Workout Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

## Request/Response Examples

### Create Exercise

**Request:**
```json
POST /exercises
{
  "name": "Bench Press",
  "category": "Upper Body",
  "equipment_needed": true
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Bench Press",
  "category": "Upper Body",
  "equipment_needed": true,
  "created_at": "2026-04-22T19:30:00"
}
```

### Create Workout

**Request:**
```json
POST /workouts
{
  "date": "2026-04-20",
  "duration_minutes": 60,
  "notes": "Upper body day"
}
```

### Add Exercise to Workout

**Request:**
```json
POST /workouts/1/exercises/1/workout_exercises
{
  "reps": 10,
  "sets": 4
}
```

## Validations

### Table Constraints
- Exercise name cannot be empty
- Unique constraint on (name, category)
- Workout duration must be positive
- WorkoutExercise must have at least reps, sets, or duration_seconds
- All WorkoutExercise values must be positive if provided

### Model Validations
- Name and category must be non-empty strings
- Workout date cannot be in the future
- WorkoutExercise values must be positive integers if provided

### Schema Validations
- Mirrors model validations
- Duration cannot exceed 24 hours (1440 minutes)