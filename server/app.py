"""
Flask application for the workout tracking API.
"""
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema,
    ExerciseDetailSchema, WorkoutDetailSchema
)
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Schema instances
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)


# ==================== Exercise Endpoints ====================

@app.route('/exercises', methods=['GET'])
def get_exercises():
    """GET /exercises - List all exercises."""
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)


@app.route('/exercises/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    """GET /exercises/<id> - Show a single exercise with associated workouts."""
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    return make_response(exercise_detail_schema.dump(exercise), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    """POST /exercises - Create a new exercise."""
    try:
        data = request.get_json()
        errors = exercise_schema.validate(data)
        if errors:
            return make_response(jsonify(errors), 400)

        exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data.get('equipment_needed', False)
        )
        db.session.add(exercise)
        db.session.commit()
        return make_response(exercise_schema.dump(exercise), 201)

    except ValidationError as e:
        return make_response(jsonify({'errors': e.messages}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


@app.route('/exercises/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    """DELETE /exercises/<id> - Delete an exercise and associated workout_exercises."""
    try:
        exercise = Exercise.query.get(exercise_id)
        if not exercise:
            return make_response(jsonify({'error': 'Exercise not found'}), 404)

        db.session.delete(exercise)
        db.session.commit()
        return make_response(jsonify({}), 204)

    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


# ==================== Workout Endpoints ====================

@app.route('/workouts', methods=['GET'])
def get_workouts():
    """GET /workouts - List all workouts."""
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)


@app.route('/workouts/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    """GET /workouts/<id> - Show a single workout with its associated exercises."""
    workout = Workout.query.get(workout_id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    return make_response(workout_detail_schema.dump(workout), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    """POST /workouts - Create a new workout."""
    try:
        data = request.get_json()
        errors = workout_schema.validate(data)
        if errors:
            return make_response(jsonify(errors), 400)

        workout = Workout(
            date=data['date'],
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes', '')
        )
        db.session.add(workout)
        db.session.commit()
        return make_response(workout_schema.dump(workout), 201)

    except ValidationError as e:
        return make_response(jsonify({'errors': e.messages}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


@app.route('/workouts/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    """DELETE /workouts/<id> - Delete a workout and associated workout_exercises."""
    try:
        workout = Workout.query.get(workout_id)
        if not workout:
            return make_response(jsonify({'error': 'Workout not found'}), 404)

        db.session.delete(workout)
        db.session.commit()
        return make_response(jsonify({}), 204)

    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


# ==================== WorkoutExercise Endpoints ====================

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    """POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises - Add an exercise to a workout."""
    try:
        workout = Workout.query.get(workout_id)
        if not workout:
            return make_response(jsonify({'error': 'Workout not found'}), 404)

        exercise = Exercise.query.get(exercise_id)
        if not exercise:
            return make_response(jsonify({'error': 'Exercise not found'}), 404)

        data = request.get_json()
        errors = workout_exercise_schema.validate(data)
        if errors:
            return make_response(jsonify(errors), 400)

        existing = WorkoutExercise.query.filter_by(
            workout_id=workout_id,
            exercise_id=exercise_id
        ).first()
        if existing:
            return make_response(
                jsonify({'error': 'This exercise is already in this workout'}),
                400
            )

        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(workout_exercise)
        db.session.commit()
        return make_response(workout_exercise_schema.dump(workout_exercise), 201)

    except ValidationError as e:
        return make_response(jsonify({'errors': e.messages}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


# Error handlers

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return make_response(jsonify({'error': 'Resource not found'}), 404)


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return make_response(jsonify({'error': 'Internal server error'}), 500)


if __name__ == '__main__':
    app.run(port=5555, debug=True)