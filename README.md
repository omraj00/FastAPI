# FastAPI Multi-Tenant Blog Tracker

A FastAPI project with multi-tenancy support that tracks page views on a blog website. The system captures and stores identity ID from cookies, page URL, and session ID whenever a page is loaded.

## Features

- Multi-tenant architecture
- Blog page template
- JavaScript tracking of page load events
- Data storage for analytics
- RESTful API endpoints

## Project Structure

```
fastapi_blog_tracker/
├── app/
│   ├── api/
│   │   ├── routes.py
│   │   └── server.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   └── base.py
│   ├── models/
│   │   ├── tenant.py
│   │   └── page_view.py
│   ├── schemas/
│   │   ├── tenant.py
│   │   └── page_view.py
│   ├── static/
│   │   └── js/
│   │       └── tracker.js
│   └── templates/
│       └── blog.html
├── init_db.py
├── main.py
├── requirements.txt
└── README.md
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
