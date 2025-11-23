import sys
from datetime import datetime, date
from db import get_exercises, get_latest_workout_for_exercise, insert_workout

def input_date(prompt="Дата тренировки (ГГГГ-ММ-ДД, по умолчанию сегодня): "):
	s = input(prompt).strip()
	if not s:
		return date.today()
	try:
		return datetime.strptime(s, "%Y-%m-%d").date()
	except ValueError:
		print("Неверный формат даты. Используйте ГГГГ-ММ-ДД")
		return input_date(prompt)

def input_int(prompt, min_val=1):
	while True:
		try:
			val = int(input(prompt))
			if val < min_val:
				raise ValueError
			return val
		except ValueError:
			print(f"Введите целое число ≥ {min_val}")

def input_float(prompt, min_val=0.0):
	while True:
		try:
			val = float(input(prompt))
			if val < min_val:
				raise ValueError
			return round(val, 2)
		except ValueError:
			print(f"Введите число ≥ {min_val}")

def main():
	print("🏋️  Gym Tracker — отслеживаем прогресс\n")

	exercises = get_exercises()
	if not exercises:
		print("Справочник упражнений пуст. Проверьте инициализацию БД.")
		return

	print("Выберите упражнение:")
	for i, ex in enumerate(exercises, 1):
		print(f"{i}. {ex['name']}")
	print()

	choice = input_int("→ Номер упражнения: ", min_val=1)
	if choice > len(exercises):
		print("Неверный номер")
		return
	ex = exercises[choice - 1]
	exercise_id = ex['id']
	print(f"\nВыбрано: {ex['name']}\n")

	workout_date = input_date()
	sets = input_int("Количество подходов: ")
	reps = input_int("Повторений в каждом подходе: ")
	weight = input_float("Вес (кг): ")

	volume = sets * reps * weight

	# Последняя запись по этому упражнению
	last = get_latest_workout_for_exercise(exercise_id)

	print("\n Расчёт:")
	print(f"Объём тренировки = {sets} × {reps} × {weight} = {volume:.1f} кг")

	if last:
		last_vol = last['volume_kg']
		last_date = last['workout_date']
		print(f"Предыдущий объём ({last_date}): {last_vol:.1f} кг")
		if volume > last_vol:
			print("Объём вырос.")
		elif volume == last_vol:
			print("На том же уровне.")
		else:
			print("Объём снизился.")
	else:
		print("Первая запись для этого упражнения!")

	# Сохраняем
	insert_workout(exercise_id, workout_date, sets, reps, weight)
	print("\n Данные сохранены!")

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\n\n Выход.")
		sys.exit(0)