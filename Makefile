.PHONY: start stop logs status test lint format clean

start:
	docker compose --profile jobs build
	docker compose up --detach

stop:
	docker compose down

logs:
	docker compose logs --follow

status:
	docker compose ps --all

test:
	PYTHONPATH=src python -m unittest discover --start-directory tests --verbose

lint:
	@echo "Not implemented: lint will be introduced by a future sprint."

format:
	@echo "Not implemented: format will be introduced by a future sprint."

clean:
	@echo "Not implemented: clean will be introduced by a future sprint."
