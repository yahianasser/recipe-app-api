# URL Shortener API

A Django-based microservice that allows users to shorten URLs, redirect using shortened codes, and retrieve click statistics. The app uses Celery with Redis for background tasks and is containerized using Docker for easy deployment.

---

## API Endpoints

### POST `/api/shorten`
  Create a shortened URL.

  - **Request Body:**
    ```json
    {
      "original_url": "https://example.com"
    }
    ```

  - **Response:**
  ```json
    {
      "shortened_url": "/api/abc123"
    }
  ```

### GET `/api/<shortened_code>`
  Redirect to the original URL.

  - **Response:**

  HTTP 302 Redirect to the original URL

### GET `/api/stats/<shortened_code>`
  Retrieve usage statistics for a shortened URL.

  - **Response:**
  ```json
  {
    "original_url": "https://example.com",
    "shortened_code": "abc123",
    "clicks": 12,
    "created_at": "2025-07-01T12:00:00Z",
    "last_accessed": "2025-07-01T13:00:00Z"
  }
  ```

## How to Run
  - Make Sure Docker is installed then run:
  ```code
    docker-compose build
    docker-compose up
  ```

### Run Tests:
  ```docker-compose run --rm app sh -c "/py/bin/python manage.py test"```