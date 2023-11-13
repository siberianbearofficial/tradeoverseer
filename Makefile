.PHONY:	build-backend
build-backend:
	cd backend && make build

.PHONY:	build-frontend
build-frontend:
	cd frontend && make build

.PHONY:	build
build:	build-backend build-frontend
	docker compose build

