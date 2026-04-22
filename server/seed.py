#!/usr/bin/env python3
"""
Seed script to populate the database with sample data.
Clears existing data and creates fresh records for testing.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date, timedelta


def seed_database():
    """Clear existing data and seed the database with sample data."""
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        WorkoutExercise.query.delete()
        Workout.query.delete()
        Exercise.query.delete()
        db.session.commit()
        print("✓ Cleared existing data\n")

        # Create exercises
        print("Creating exercises...")
        exercises = [
            Exercise(
                name="Barbell Squat",
                category="Lower Body",
                equipment_needed=True
            ),
            Exercise(
                name="Bench Press",
                category="Upper Body",
                equipment_needed=True
            ),
            Exercise(
                name="Deadlift",
                category="Full Body",
                equipment_needed=True
            ),
            Exercise(
                name="Pull-ups",
                category="Upper Body",
                equipment_needed=False
            ),
            Exercise(
                name="Running",
                category="Cardio",
                equipment_needed=False
            ),
            Exercise(
                name="Dumbbell Rows",
                category="Upper Body",
                equipment_needed=True
            ),
            Exercise(
                name="Plank",
                category="Core",
                equipment_needed=False
            ),
            Exercise(
                name="Cycling",
                category="Cardio",
                equipment_needed=True
            ),
        ]

        for exercise in exercises:
            db.session.add(exercise)
        db.session.commit()
        print(f"✓ Created {len(exercises)} exercises\n")

        # Create workouts
        print("Creating workouts...")
        today = date.today()
        workouts = [
            Workout(
                date=today - timedelta(days=5),
                duration_minutes=60,
                notes="Upper body strength day. Felt good, great pump."
            ),
            Workout(
                date=today - timedelta(days=4),
                duration_minutes=45,
                notes="Leg day. Heavy squats and deadlifts."
            ),
            Workout(
                date=today - timedelta(days=3),
                duration_minutes=30,
                notes="Cardio session. 5K run on treadmill."
            ),
            Workout(
                date=today - timedelta(days=2),
                duration_minutes=75,
                notes="Push/pull day. Bench, rows, and pull-ups."
            ),
            Workout(
                date=today - timedelta(days=1),
                duration_minutes=40,
                notes="Core and stability work."
            ),
        ]

        for workout in workouts:
            db.session.add(workout)
        db.session.commit()
        print(f"✓ Created {len(workouts)} workouts\n")

        # Create workout exercises (associations)
        print("Creating workout exercise associations...")
        workout_exercises = [
            # Workout 1 (Upper body)
            WorkoutExercise(
                workout_id=1,
                exercise_id=2,  # Bench Press
                reps=5,
                sets=5,
                duration_seconds=None
            ),
            WorkoutExercise(
                workout_id=1,
                exercise_id=6,  # Dumbbell Rows
                reps=8,
                sets=4,
                duration_seconds=None
            ),
            WorkoutExercise(
                workout_id=1,
                exercise_id=4,  # Pull-ups
                reps=10,
                sets=4,
                duration_seconds=None
            ),
            # Workout 2 (Legs)
            WorkoutExercise(
                workout_id=2,
                exercise_id=1,  # Barbell Squat
                reps=6,
                sets=5,
                duration_seconds=None
            ),
            WorkoutExercise(
                workout_id=2,
                exercise_id=3,  # Deadlift
                reps=3,
                sets=5,
                duration_seconds=None
            ),
            # Workout 3 (Cardio)
            WorkoutExercise(
                workout_id=3,
                exercise_id=5,  # Running
                reps=None,
                sets=None,
                duration_seconds=1800  # 30 minutes
            ),
            # Workout 4 (Push/Pull)
            WorkoutExercise(
                workout_id=4,
                exercise_id=2,  # Bench Press
                reps=8,
                sets=4,
                duration_seconds=None
            ),
            WorkoutExercise(
                workout_id=4,
                exercise_id=6,  # Dumbbell Rows
                reps=8,
                sets=4,
                duration_seconds=None
            ),
            WorkoutExercise(
                workout_id=4,
                exercise_id=4,  # Pull-ups
                reps=12,
                sets=3,
                duration_seconds=None
            ),
            # Workout 5 (Core)
            WorkoutExercise(
                workout_id=5,
                exercise_id=7,  # Plank
                reps=None,
                sets=3,
                duration_seconds=60
            ),
        ]

        for we in workout_exercises:
            db.session.add(we)
        db.session.commit()
        print(f"✓ Created {len(workout_exercises)} workout exercise associations\n")

        print("=" * 50)
        print("✅ Database seeded successfully!")
        print("=" * 50)


if __name__ == '__main__':
    seed_database()
