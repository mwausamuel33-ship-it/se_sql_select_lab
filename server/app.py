import os
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, ExerciseDetailSchema, WorkoutSchema, WorkoutDetailSchema, WorkoutExerciseSchema
from marshmallow import ValidationError

app = Flask(__name__)

# set up the database path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "instance", "app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# create schema instances to use in routes
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()

workout_exercise_schema = WorkoutExerciseSchema()


# --- Exercise routes ---

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)


@app.route('/exercises/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    return make_response(exercise_detail_schema.dump(exercise), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()

    # validate incoming data with schema first
    errors = exercise_schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)

    try:
        exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data.get('equipment_needed', False)
        )
        db.session.add(exercise)
        db.session.commit()
        return make_response(exercise_schema.dump(exercise), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


@app.route('/exercises/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)

    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({}), 204)


# --- Workout routes ---

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)


@app.route('/workouts/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    # use detail schema so we get exercises + reps/sets/duration
    return make_response(workout_detail_schema.dump(workout), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()

    errors = workout_schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)

    try:
        workout = Workout(
            date=data['date'],
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes', '')
        )
        db.session.add(workout)
        db.session.commit()
        return make_response(workout_schema.dump(workout), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


@app.route('/workouts/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)

    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({}), 204)


# --- WorkoutExercise routes ---

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
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

    # check if this exercise is already in the workout
    already_exists = WorkoutExercise.query.filter_by(
        workout_id=workout_id,
        exercise_id=exercise_id
    ).first()
    if already_exists:
        return make_response(jsonify({'error': 'Exercise already added to this workout'}), 400)

    try:
        we = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(we)
        db.session.commit()
        return make_response(workout_exercise_schema.dump(we), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
