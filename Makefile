.PHONY: start stop logs status test lint format clean

start:
	docker compose up --build --detach

stop:
	docker compose down

logs:
	docker compose logs --follow

status:
	docker compose ps --all

test:
	@echo "Not implemented: no test suite is configured yet." >&2
	@exit 1

lint:
	@echo "Not implemented: lint will be introduced by a future sprint."

format:
	@echo "Not implemented: format will be introduced by a future sprint."

clean:
	@echo "Not implemented: clean will be introduced by a future sprint."
