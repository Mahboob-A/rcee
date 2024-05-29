

# ### Docker management commands 
 
docker-up: 
	docker compose -p rce_engine -f dev.yml up --build -d --remove-orphans 

docker-down: 
	docker compose -p rce_engine -f dev.yml down

docker-down-v: 
	docker compose -p rce_engine -f dev.yml down -v

docker-logs: 
	docker compose -p rce_engine -f dev.yml logs 

docker-logs-rce-engine: 
	docker compose -p rce_engine -f dev.yml logs rce-judge-engine

docker-restart-rce-engine: 
	docker compose -p rce_engine -f dev.yml restart rce-judge-engine

docker-exec-rce-engine: 
	docker compose -p rce_engine -f dev.yml exec rce-judge-engine /bin/bash 

# ## 



# ### Django Commands

makemigrations: 
	docker compose -p rce_engine -f dev.yml run --rm rce-judge-engine python manage.py makemigrations

migrate: 
	docker compose -p rce_engine -f dev.yml run --rm rce-judge-engine python manage.py migrate

collectstatic: 
	docker compose -p rce_engine -f dev.yml run --rm rce-judge-engine python manage.py collectstatic --no-input --clear 

superuser: 
	docker compose -p rce_engine -f dev.yml run --rm rce-judge-engine python manage.py createsuperuser 

# ## 




# ### Pytest Commands
pytest-no-wrn-codecov:
	docker compose -p rce_engine -f dev.yml run --rm rce-judge-engine pytest -p no:warnigns --cov=. -v  

pytest-no-wrn-codecov-html:
	docker compose -p rce_engine -f dev.yml run --rm rce-judge-engine pytest -p no:warnigns --cov=. --cov-report html



# ### Other Tools for Formatting 

flake8: 
	docker compose -p rce_engine -f dev.yml exec rce-judge-engine flake8 . 

black-check: 
	docker compose -p rce_engine -f dev.yml exec rce-judge-engine black --check --exclude=migrations . 

black-diff: 
	docker compose -p rce_engine -f dev.yml exec rce-judge-engine black --diff --exclude=migrations . 

black: 
	docker compose -p rce_engine -f dev.yml exec rce-judge-engine black --exclude=migrations . 

isort-check: 
	docker compose -p rce_engine -f dev.yml exec rce-judge-engine isort . --check-only --skip venv --skip migrations 

isort-diff: 
	docker compose -p rce_engine -f dev.yml exec rce-judge-engine isort . --diff --skip venv --skip migrations

isort: 
	docker compose -p rce_engine -f dev.yml exec rce-judge-engine isort . --skip venv --skip migrations

# ## 