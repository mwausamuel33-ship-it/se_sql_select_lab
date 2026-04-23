# Workout Tracking API

A Flask-based backend API for tracking workouts and exercises. Personal trainers use this API to manage their clients' workout data, including exercises with sets, reps, and duration information.

## Description

This API provides full CRUD operations for Exercises and Workouts, and allows adding exercises to workouts with sets, reps, and duration tracking. It uses Flask, SQLAlchemy, and Marshmallow with validations enforced at the database, model, and schema levels.

## Installation

**Prerequisites:** Python 3.8+, pipenv

```bash
# 1. Clone the repo and navigate into it
git clone <your-repo-url>
cd se_sql_select_lab

# 2. Install dependencies
pipenv install

# 3. Activate the virtual environment
pipenv shell

# 4. Run database migrations
cd server
PYTHONPATH=. FLASK_APP=app.py flask db upgrade

# 5. Seed the database
PYTHONPATH=. python seed.py
```

## Running the API

```bash
cd server
PYTHONPATH=. FLASK_APP=app.py flask run --port=5555
```

Or run directly:

```bash
cd server
PYTHONPATH=. python app.py
```

The API will be available at `http://localhost:5555`.

## API Endpoints

### Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get a single exercise with its associated workouts |
| POST | `/exercises` | Create a new exercise |
| DELETE | `/exercises/<id>` | Delete an exercise and its workout associations |

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Get a single workout with exercises and sets/reps/duration |
| POST | `/workouts` | Create a new workout |
| DELETE | `/workouts/<id>` | Delete a workout and its exercise associations |

### Workout Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout with reps/sets/duration |

## Request Examples

### POST /exercises
```json
{
  "name": "Bench Press",
  "category": "Upper Body",
  "equipment_needed": true
}
```

### POST /workouts
```json
{
  "date": "2026-04-20",
  "duration_minutes": 60,
  "notes": "Upper body day"
}
```

### POST /workouts/1/exercises/1/workout_exercises
```json
{
  "reps": 10,
  "sets": 4
}
```

## Validations

### Table Constraints
- Exercise name cannot be empty
- Unique constraint on (name, category) pair
- Workout duration must be positive
- WorkoutExercise must have at least one of reps, sets, or duration_seconds
- All WorkoutExercise numeric values must be positive if provided

### Model Validations
- Exercise name and category must be non-empty strings
- Workout date cannot be in the future
- WorkoutExercise reps, sets, and duration_seconds must be positive integers if provided

### Schema Validations
- Mirrors model validations on incoming request data
- Workout duration cannot exceed 1440 minutes (24 hours)
- At least one of reps, sets, or duration_seconds required when adding exercise to workout
