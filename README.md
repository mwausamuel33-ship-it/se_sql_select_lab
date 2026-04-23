# Workout Tracking API

A Flask-based REST API for tracking workouts and exercises. Built for personal trainers to manage client workout data including exercises, sets, reps, and duration.

## Description

This API provides full CRUD operations for Exercises and Workouts, and allows adding exercises to workouts with sets, reps, and duration tracking. It is built with Flask, SQLAlchemy, and Marshmallow with validations enforced at the database, model, and schema levels.

---

## Prerequisites

Make sure you have the following installed before getting started:

- Python 3.8+
- pip
- pipenv

To install pipenv if you don't have it:

```bash
pip install pipenv
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mwausamuel33-ship-it/se_sql_select_lab.git
cd se_sql_select_lab
```

### 2. Install dependencies

```bash
pipenv install
```

This will install all required packages from the Pipfile including Flask, Flask-Migrate, Flask-SQLAlchemy, Werkzeug, and Marshmallow.

### 3. Activate the virtual environment

```bash
pipenv shell
```

You should see your terminal prompt change to show the virtual environment is active.

### 4. Navigate into the server directory

```bash
cd server
```

### 5. Set up the database

Run the migrations to create the database tables:

```bash
PYTHONPATH=. FLASK_APP=app.py flask db upgrade
```

### 6. Seed the database

Populate the database with sample exercises and workouts:

```bash
PYTHONPATH=. python seed.py
```

You should see output like:

```
Clearing old data...
Created exercises
Created workouts
Created workout exercises

Done! Database seeded successfully.
```

---

## Running the API

From inside the `server/` directory with the virtual environment active:

```bash
PYTHONPATH=. FLASK_APP=app.py flask run --port=5555
```

Or run the app directly:

```bash
PYTHONPATH=. python app.py
```

The API will be available at: **http://localhost:5555**

---

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

---

## Request & Response Examples

### GET /exercises
```json
[
  {
    "id": 1,
    "name": "Barbell Squat",
    "category": "Lower Body",
    "equipment_needed": true
  }
]
```

### POST /exercises
Request body:
```json
{
  "name": "Bench Press",
  "category": "Upper Body",
  "equipment_needed": true
}
```
Response (201):
```json
{
  "id": 2,
  "name": "Bench Press",
  "category": "Upper Body",
  "equipment_needed": true
}
```

### POST /workouts
Request body:
```json
{
  "date": "2026-04-20",
  "duration_minutes": 60,
  "notes": "Upper body day"
}
```

### POST /workouts/1/exercises/1/workout_exercises
Request body:
```json
{
  "reps": 10,
  "sets": 4
}
```
Response (201):
```json
{
  "id": 1,
  "workout_id": 1,
  "exercise_id": 1,
  "reps": 10,
  "sets": 4,
  "duration_seconds": null
}
```

---

## Validations

### Table Constraints
- Exercise name cannot be empty
- Unique constraint on (name, category) pair — no duplicate exercise names within the same category
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
- At least one of reps, sets, or duration_seconds is required when adding an exercise to a workout

---

## Resetting the Database

To wipe and re-seed the database at any time, just run the seed file again:

```bash
cd server
PYTHONPATH=. python seed.py
```

---

## Project Structure

```
se_sql_select_lab/
├── server/
│   ├── app.py          # Flask app and all route definitions
│   ├── models.py       # SQLAlchemy models with validations
│   ├── schemas.py      # Marshmallow schemas for serialization
│   ├── seed.py         # Database seed script
│   └── migrations/     # Flask-Migrate migration files
├── Pipfile
└── README.md
```
