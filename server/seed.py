#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date, timedelta

with app.app_context():
    # clear out old data so we start fresh every time
    print("Clearing old data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    # create some exercises
    squat = Exercise(name="Barbell Squat", category="Lower Body", equipment_needed=True)
    bench = Exercise(name="Bench Press", category="Upper Body", equipment_needed=True)
    deadlift = Exercise(name="Deadlift", category="Full Body", equipment_needed=True)
    pullups = Exercise(name="Pull-ups", category="Upper Body", equipment_needed=False)
    running = Exercise(name="Running", category="Cardio", equipment_needed=False)
    rows = Exercise(name="Dumbbell Rows", category="Upper Body", equipment_needed=True)
    plank = Exercise(name="Plank", category="Core", equipment_needed=False)
    cycling = Exercise(name="Cycling", category="Cardio", equipment_needed=True)

    db.session.add_all([squat, bench, deadlift, pullups, running, rows, plank, cycling])
    db.session.commit()
    print("Created exercises")

    # create some workouts using past dates
    today = date.today()

    w1 = Workout(date=today - timedelta(days=5), duration_minutes=60, notes="Upper body strength day")
    w2 = Workout(date=today - timedelta(days=4), duration_minutes=45, notes="Leg day - heavy squats and deadlifts")
    w3 = Workout(date=today - timedelta(days=3), duration_minutes=30, notes="Cardio - 5k run")
    w4 = Workout(date=today - timedelta(days=2), duration_minutes=75, notes="Push/pull day")
    w5 = Workout(date=today - timedelta(days=1), duration_minutes=40, notes="Core and stability")

    db.session.add_all([w1, w2, w3, w4, w5])
    db.session.commit()
    print("Created workouts")

    # link exercises to workouts with reps/sets/duration
    db.session.add_all([
        WorkoutExercise(workout=w1, exercise=bench, reps=5, sets=5),
        WorkoutExercise(workout=w1, exercise=rows, reps=8, sets=4),
        WorkoutExercise(workout=w1, exercise=pullups, reps=10, sets=4),
        WorkoutExercise(workout=w2, exercise=squat, reps=6, sets=5),
        WorkoutExercise(workout=w2, exercise=deadlift, reps=3, sets=5),
        WorkoutExercise(workout=w3, exercise=running, duration_seconds=1800),
        WorkoutExercise(workout=w4, exercise=bench, reps=8, sets=4),
        WorkoutExercise(workout=w4, exercise=rows, reps=8, sets=4),
        WorkoutExercise(workout=w4, exercise=pullups, reps=12, sets=3),
        WorkoutExercise(workout=w5, exercise=plank, sets=3, duration_seconds=60),
    ])
    db.session.commit()
    print("Created workout exercises")

    print("\nDone! Database seeded successfully.")
