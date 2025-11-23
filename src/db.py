import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_connection():
	return psycopg2.connect(
		host=os.getenv('DB_HOST', 'localhost'),
		port=os.getenv('DB_PORT', '5432'),
		dbname=os.getenv('DB_NAME', 'gym'),
		user=os.getenv('DB_USER', 'user'),
		password=os.getenv('DB_PASSWORD', 'password')
	)

def get_exercises():
	with get_connection() as conn:
		with conn.cursor(cursor_factory=RealDictCursor) as cur:
			cur.execute("SELECT id, name FROM gym.exercises ORDER BY name")
			return cur.fetchall()

def get_latest_workout_for_exercise(exercise_id):
	with get_connection() as conn:
		with conn.cursor(cursor_factory=RealDictCursor) as cur:
			cur.execute("""
				SELECT sets, reps, weight_kg, volume_kg, workout_date
				FROM gym.workouts
				WHERE exercise_id = %s
				ORDER BY workout_date DESC, created_at DESC
				LIMIT 1
			""", (exercise_id,))
			return cur.fetchone()

def insert_workout(exercise_id, workout_date, sets, reps, weight_kg):
	with get_connection() as conn:
		with conn.cursor() as cur:
			cur.execute("""
				INSERT INTO gym.workouts (exercise_id, workout_date, sets, reps, weight_kg)
				VALUES (%s, %s, %s, %s, %s)
			""", (exercise_id, workout_date, sets, reps, weight_kg))
			conn.commit()