# ArticleRater

**ArticleRater** is a Django-based REST API service that allows users to register, log in, view articles, and rate them. The project uses Django REST Framework for API endpoints, a custom user model, JWT-based authentication, PostgreSQL as the database, and Redis as a caching layer. It also integrates Celery for asynchronous background tasks, periodically processing rating updates to handle high load and smooth out sudden rating spikes.

## Features

- **Custom User Model**: Extends Django’s `AbstractUser`, allowing for customization.
- **Article Management**:  
  - Create and view articles.
  - Each article stores aggregated rating information (count and sum) for efficient retrieval.
- **Rating System**:  
  - Authenticated users can rate articles with a score from 1 to 5.
  - If a user re-rates an article, the previous rating is updated.
  - Ratings are not immediately applied to the article’s aggregates; instead, they are batched and processed periodically to improve performance and handle spikes.
- **JWT Authentication**:  
  - Register a new user: `/api/auth/register/`
  - Obtain JWT tokens by logging in: `/api/auth/login/`
  - Refresh access tokens: `/api/auth/refresh/`
- **High Performance & Scalability**:
  - Uses Redis to queue rating updates, avoiding immediate heavy database writes.
  - Celery tasks run periodically to update article rating aggregates in batch.
  - This approach smooths out short-term rating surges and maintains performance under heavy load.
- **Periodic Tasks with Celery & Redis**:  
  - The `apply_rating_updates` task runs at intervals (configurable) to process accumulated rating changes.
  - Uses `django_celery_beat` to manage schedules directly from the Django admin or from code.

## Technology Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Caching & Queues**: Redis
- **Asynchronous Tasks**: Celery with `django_celery_beat`
- **Authentication**: JWT via `djangorestframework-simplejwt`
- **Containerization (Optional)**: Docker & Docker Compose

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Mohammadreza-kh94/article-rater.git
   cd ArticleRater
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root. For example:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key

   DATABASE_NAME=postgres_db
   DATABASE_USER=postgres_db
   DATABASE_PASSWORD=postgres_db
   DATABASE_HOST=localhost
   DATABASE_PORT=5432

   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=1
   ```

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server**:
   ```bash
   python manage.py runserver
   ```

   The API is now accessible at `http://127.0.0.1:8000/api/`

### Running Celery & Celery Beat

Open two separate terminals:

- **Celery Worker**:
  ```bash
  celery -A articlerater worker -l info
  ```

- **Celery Beat** (for periodic tasks):
  ```bash
  celery -A articlerater beat -l info
  ```

### Docker & Docker Compose

You can also use Docker and Docker Compose:

```bash
docker-compose up --build
```

This will start:
- PostgreSQL
- Redis
- Django web service
- Celery worker
- Celery beat

### Endpoints Overview

- **User Registration**: `POST /api/auth/register/`
  ```json
  {
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "MyStrongPassword123",
    "password2": "MyStrongPassword123"
  }
  ```

- **Login & Obtain Tokens**: `POST /api/auth/login/`
  ```json
  {
    "username": "newuser",
    "password": "MyStrongPassword123"
  }
  ```

- **Refresh Token**: `POST /api/auth/refresh/`

- **Articles**:  
  - `GET /api/articles/` - List articles with title, rating count, average rating, and user’s rating if authenticated.
  - `POST /api/articles/` - Create an article (requires authentication).

- **Ratings**:
  - `POST /api/ratings/`
  ```json
  {
    "article_id": 1,
    "score": 5
  }
  ```
  Updates or creates the user’s rating for that article.

### Performance Considerations

- Ratings are stored in Redis lists and processed periodically via Celery tasks.
- This design prevents immediate heavy writes and mitigates flash-mob rating attacks.
- The aggregated rating data (count & sum) on the `Article` model ensures quick average rating calculations.

### Testing

- **Run tests**:
  ```bash
  python manage.py test
  ```
