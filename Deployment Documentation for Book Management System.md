# Deployment Documentation

This guide provides step-by-step instructions for deploying the Book Management System. By following these steps, you will clone the repository, set up the environment, run the application, and access the API endpoints.

---

## Prerequisites

Before you begin, ensure the following software and tools are installed and running:

1. **Docker and Docker Compose**:
   - Required to containerize the application and its dependencies.
   - Install them if not already present:
     - [Install Docker](https://docs.docker.com/get-docker/)
     - [Install Docker Compose](https://docs.docker.com/compose/install/)

2. **Ollama Server**:
   - Must be running on your host machine at `http://localhost:11434/api/generate` with the LLaMA 3.1:8b model.
   - Setup instructions:
     - Install Ollama from the [Ollama GitHub repository](https://github.com/jmorganca/ollama).
     - Start the server:
       ```bash
       ollama serve --model llama3.1:8b
       ```
     - Verify it’s running by sending a test request:
       ```bash
       curl -X POST http://localhost:11434/api/generate -d '{"model": "llama3.1:8b", "prompt": "Test prompt"}'
       ```

---

## Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone <repository_url>
cd book-management-system
```

Replace `<repository_url>` with the actual URL of the repository.

---

## Step 2: Set Up the Environment

1. **Verify Docker and Docker Compose**:
   - Check Docker:
     ```bash
     docker --version
     ```
   - Check Docker Compose:
     ```bash
     docker-compose --version
     ```

2. **Verify Ollama Server**:
   - Ensure the Ollama server is running and accessible at `http://localhost:11434/api/generate` (see Prerequisites).

---

## Step 3: Run the Application

Use Docker Compose to build and run the application and its PostgreSQL database:

1. **Build and Start the Containers**:
   - From the `book_management_system` directory, run:
     ```bash
     docker-compose up --build
     ```
   - This builds the application image and starts the app (port 8000) and database (port 5432).

2. **Check Container Status**:
   - Verify both services are running:
     ```bash
     docker-compose ps
     ```
   - Look for `app` and `db` in the "Up" state.

---

## Step 4: Access the API

The API is available at `http://localhost:8000`. Use tools like `curl`, Postman, or the Swagger UI to interact with it.

1. **Swagger Documentation**:
   - Visit:
     ```
     http://localhost:8000/docs
     ```
   - Explore and test endpoints interactively.

2. **Key Endpoints**:
   - `POST /books`: Add a new book.
   - `GET /books`: List all books.
   - `GET /books/<id>`: Get a specific book.
   - `PUT /books/<id>`: Update a book.
   - `DELETE /books/<id>`: Delete a book.
   - `POST /books/<id>/reviews`: Add a review.
   - `GET /books/<id>/reviews`: List reviews for a book.
   - `GET /books/<id>/summary`: Get summary and rating.
   - `GET /recommendations?genre=<genre>`: Get recommendations.
   - `POST /generate-summary`: Generate a summary.

---

## Step 5: Authentication

Protected endpoints require a JWT token in the `Authorization` header.

1. **Generate a Token**:
   - Manually generate a token using `create_access_token` in `app/utils/auth.py` with `{"sub": "testuser"}`.
   - Alternatively, implement a `/token` endpoint.

2. **Use the Token**:
   - Include it in requests:
     ```
     Authorization: Bearer <your_jwt_token>
     ```

---

## Troubleshooting

- **Cannot connect to Ollama server**:
  - Ensure it’s running at `http://localhost:11434/api/generate`.
- **Database connection errors**:
  - Check the PostgreSQL container:
    ```bash
    docker-compose logs db
    ```
  - Verify `DATABASE_URL` in `docker-compose.yml`.
- **Application fails to start**:
  - Rebuild the image:
    ```bash
    docker-compose build
    ```
- **JWT authentication fails**:
  - Confirm token validity and header format.

---

## Additional Notes

- **Stop the Application**:
  ```bash
  docker-compose down
  ```
- **Rebuild After Changes**:
  ```bash
  docker-compose up --build
  ```
- **Database Access**:
  - Host: `localhost`
  - Port: `5432`
  - Database: `bookdb`
  - Username: `user`
  - Password: `password`

---

Follow these steps to deploy the Book Management System successfully. For further assistance, consult the project documentation or contact the development team.