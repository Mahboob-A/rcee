

# ### Docker management commands 
 
docker-up: 
	docker compose -p rce_engine -f production.yml up --build -d --remove-orphans 

docker-down: 
	docker compose -p rce_engine -f production.yml down

docker-logs: 
	docker compose -p rce_engine -f production.yml logs 

docker-logs-rce-engine: 
	docker compose -p rce_engine -f production.yml logs rce-judge-engine

docker-restart-rce-engine: 
	docker compose -p rce_engine -f production.yml restart rce-judge-engine

docker-exec-rce-engine: 
	docker compose -p rce_engine -f production.yml exec rce-judge-engine /bin/bash 

# ## 
