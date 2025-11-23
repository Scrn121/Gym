from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import date
from db import get_exercises, get_latest_workout, insert_workout, get_workout_history, get_previous_workout

app = FastAPI()
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
	exercises = get_exercises()
	return templates.TemplateResponse("index.html", {
		"request": request,
		"exercises": exercises,
		"date": date.today().isoformat()
	})

@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):
	try:
		records = get_workout_history()
		return templates.TemplateResponse("history.html", {
			"request": request,
			"records": records
		})
	except Exception as e:
		return f"<pre style='background:#fee; color:#700; padding:1rem; border-radius:4px;'>Ошибка: {str(e)}</pre>"

@app.post("/record")
async def record_workout(
	request: Request,
	exercise_id: int = Form(...),
	workout_date: str = Form(...),
	sets: int = Form(...),
	reps: int = Form(...),
	weight_kg: float = Form(...)
):
	# Преобразуем дату
	d = date.fromisoformat(workout_date)

	# Сначала получаем ПРЕДЫДУЩУЮ запись (до вставки!)
	prev = get_previous_workout(exercise_id)

	# Потом сохраняем новую
	insert_workout(exercise_id, d, sets, reps, weight_kg)

	# Считаем текущий объём
	current_volume = sets * reps * weight_kg

	# Сравниваем с ПРЕДЫДУЩЕЙ
	if prev and prev['volume_kg'] is not None:
		prev_vol = float(prev['volume_kg'])
		if current_volume > prev_vol:
			message = f"✅ ПРОГРЕСС! Объём вырос с {prev_vol:.1f} → {current_volume:.1f} кг"
		elif current_volume < prev_vol:
			message = f"⚠️ Регресс: с {prev_vol:.1f} → {current_volume:.1f} кг"
		else:
			message = f"➖ На том же уровне: {current_volume:.1f} кг"
	else:
		message = "🆕 Первая запись для этого упражнения"

	exercises = get_exercises()
	return templates.TemplateResponse("index.html", {
		"request": request,
		"exercises": exercises,
		"date": d.isoformat(),
		"message": message,
		"success": True
	})