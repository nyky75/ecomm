.PHONY: test report down stop-all

test:
	docker-compose run --rm tests

report:
	@if [ ! -d "allure-results" ] || [ -z "$$(ls -A allure-results 2>/dev/null)" ]; then \
		echo ">> Результатов нет — запускаем тесты перед отчётом..."; \
		docker-compose run --rm tests; \
	fi
	@echo ">> Запускаем Allure UI: http://localhost:5050/allure-docker-service/latest-report"
	docker-compose up allure

down:
	docker-compose down

stop-all:
	docker stop $$(docker ps -q) || true
