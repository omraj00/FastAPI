# FastAPI Multi-Tenant Blog Tracker

A FastAPI project with multi-tenancy support that tracks page views on a blog website. The system captures and stores identity ID from cookies, page URL, and session ID whenever a page is loaded. A background worker powered by Celery handles the actual logging of pageviews to reduce load on the main application.

## Features

- Multi-tenant architecture
- Blog page template
- JavaScript-based page view tracking
- Background processing with Celery
- SQLite database with SQLAlchemy
- RESTful API endpoints

## Project Structure

```
fastapi_blog_tracker/
├── app/
│   ├── __init__.py
│   ├── celery.py              # Celery app configuration
│   ├── config.py              # App-level configuration (settings, constants)
│   ├── db.py                  # SQLAlchemy DB setup and session
│   ├── models.py              # SQLAlchemy models (e.g., PageView, Tenant)
│   ├── routes.py              # API route definitions (track pageviews, blog view)
│   ├── schemas.py             # Pydantic schemas for validation
│   ├── server.py              # FastAPI app instance and route registration
│   ├── tasks.py               # Celery background tasks (e.g., track_pageview_task)
│   ├── static/
│   │   ├── blog.html          # HTML template for blog page
│   │   └── tracker.js         # JS script for sending page view events
│   └── __pycache__/           # Compiled Python cache (auto-generated)
├── fastapi_blog_tracker.db    # SQLite database file
├── Dockerfile                 # Docker config (optional)
├── requirements.txt           # Python dependencies
├── .gitignore                 # Files to ignore in version control
├── README.md                  # Project overview and usage instructions
└── main.py                    # App entry point (runs FastAPI server)

```

## Installation

1. Clone the repository
2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the requirements:

```bash
pip install -r requirements.txt
```

4. Initialize the database with sample data:

```bash
python init_db.py
```

5. Run the application:

```bash
python main.py
```

6. In a separate terminal, start the Celery worker:

```bash
celery -A app.celery.celery_app worker --loglevel=info
```

## Usage

1. Access the blog at: http://localhost:8000/api/blog

2. To test different tenants, you can modify your hosts file to add entries like:
   - tech.localhost
   - food.localhost
   - travel.localhost

   Then access the blog using these domains: http://tech.localhost:8000/api/blog

3. The JavaScript tracker will automatically capture page views and send them to the backend.

## API Endpoints

- `GET /api/blog` - View the blog page
- `POST /api/track-pageview` - Track a page view (used by the JS tracker)
- `POST /api/tenants` - Create a new tenant
- `GET /api/tenants` - List all tenants

## Multi-Tenancy

This application uses the host-based multi-tenancy approach, where different tenants are identified by different domain names. The system will automatically determine the tenant based on the domain used to access the application.
