create schema if not exists gym;

create table if not exists gym.exercises (
	ID serial primary key,
	Name varchar(255) null
);

create table if not exists gym.workouts(
	ID serial primary keym
	Exercise_ID int not null references gym.exercises(ID) on delete cascade,
	Workout_date date not null,
	sets int not null check(sets > 0),
	reps int not null check(reps > 0),
	weight_kg numeric(5,2) not null check(weight_kg >= 0),
	volume_kg as (sets * reps * weight_kg) stored,
	created_at timestamptz default now()
)
