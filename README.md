# FastAPI Job Board (My First Full Project)

A clean, modern job board API built with FastAPI, PostgreSQL, JWT auth, and Docker.

## Features (so far)
- User registration & login with secure password hashing
- JWT protected routes (`/auth/me`)
- Swagger UI with working Bearer token auth
- Alembic migrations
- Clean project structure

## Tech Stack
- FastAPI + SQLModel
- PostgreSQL (Docker)
- JWT + bcrypt
- Alembic migrations

## Quick Start
```bash
docker-compose up -d
alembic upgrade head
uvicorn jobboard_api.main:app --reload