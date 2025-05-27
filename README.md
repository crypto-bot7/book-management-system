# Book Management System
Intelligent Book Management System built with Python, FastAPI, PostgreSQL, and LLaMA 3.1 for AI-generated summaries. Features RESTful API for managing books, reviews, and recommendations, with JWT authentication and async operations. Deployable via Docker.

## Features
- Add, retrieve, update, and delete books.
- Manage user reviews for books.
- Generate book summaries using LLaMA 3.1.
- Provide book recommendations based on genre and rating.
- Asynchronous database operations with SQLAlchemy and asyncpg.
- JWT-based authentication.
- Deployable via Docker.

## Prerequisites
- Docker and Docker Compose installed.
- Ollama server running on the host machine at `http://localhost:11434/api/generate` with LLaMA 3.1:8b model.
