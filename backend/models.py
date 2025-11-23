from datetime import date
from pydantic import BaseModel, Field

class WorkoutCreate(BaseModel):
	exercise_id: int
	workout_date: date
	sets: int = Field(gt=0)
	reps: int = Field(gt=0)
	weight_kg: float = Field(ge=0)

class WorkoutResult(BaseModel):
	volume: float
	previous_volume: float | None
	previous_date: date | None
	message: str