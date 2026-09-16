# AeroSafe – Airport Noise Management API

A production-style Django REST API for managing airport noise events, inspections, assets, corrective work orders, authentication, and AI-assisted asset queries.

## Overview

AeroSafe is a simplified airport operations management system designed around the workflow of detecting and managing airport noise-related events.

The application demonstrates how an airport operations team can:

* Record noise events
* Associate noise events with airports and monitoring assets
* Review and investigate noise events
* Create inspections
* Create corrective work orders
* Assign work to operations users
* Filter, search, and sort noise records
* Authenticate users using JWT
* Control access using role-based permissions
* Use an LLM to answer questions about asset information
* Handle API validation and errors consistently

> **Note:** AeroSafe is an independent demonstration project inspired by airport operations workflows. It is not the internal implementation or source code of Aerosimple.

## Business Workflow

```text
Airport / Resident Reports Noise Event
                |
                v
           Noise Log
                |
                v
       Operations Team Review
                |
                v
           Inspection
                |
                v
          Work Order
                |
                v
       Corrective Action
                |
                v
            Resolution
```

## Architecture

```text
                    Client
                      |
                      v
                Django REST API
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
      Airports     Assets     Noise Logs
                                  |
                                  v
                             Inspections
                                  |
                                  v
                             Work Orders

                      |
                      v
                 PostgreSQL
                      |
                      v
                 LLM Service
                      |
                      v
              Local LLM / Ollama
```

## Project Structure

```text
noise-management/
│
├── config/                 # Django configuration and API routing
├── users/                  # Authentication and permissions
├── airports/               # Airport management
├── assets/                 # Airport asset management
├── noise_logs/             # Noise event management
├── inspections/            # Inspection workflow
├── workorders/             # Corrective work orders
├── llm/                    # LLM integration and AI services
│
├── manage.py
├── requirements.txt
├── .gitignore
├── AeroSafe_Architecture_Doc.pdf
└── README.md
```

## Core Data Relationships

```text
Airport
   |
   +------< Asset
   |
   +------< NoiseLog
                 |
                 +------< Inspection
                                |
                                +------< WorkOrder

User
   |
   +------< NoiseLog
   |
   +------< WorkOrder
```

## Technology Stack

* Python
* Django
* Django REST Framework
* PostgreSQL / SQL database
* Django Filter
* SimpleJWT
* drf-spectacular
* OpenAPI / Swagger
* Ollama / Local LLM
* Git / GitHub

## Key Features

### REST API

CRUD APIs are implemented using Django REST Framework ViewSets and routers.

Example:

```text
GET    /api/noise-logs/
POST   /api/noise-logs/
GET    /api/noise-logs/{id}/
PATCH  /api/noise-logs/{id}/
DELETE /api/noise-logs/{id}/
```

### Authentication

JWT authentication is implemented using Django REST Framework SimpleJWT.

Authentication flow:

```text
Username + Password
        |
        v
   Access Token
        |
        v
Authorization: Bearer <token>
        |
        v
      Django
        |
        v
   request.user
```

### Role-Based Authorization

Operations APIs use role-based permissions.

Users belonging to the `Operations` group can access operations functionality.

Authentication answers:

> Who are you?

Authorization answers:

> What are you allowed to do?

### Filtering and Search

Noise logs support structured filtering, search and ordering.

Example:

```text
/api/noise-logs/?airport=1&min_noise_level=80&ordering=-noise_level
```

This allows operations users to find high-noise events for a specific airport and sort them by noise level.

### Query Optimization

The API uses Django ORM optimization techniques such as:

```python
select_related()
prefetch_related()
```

`select_related()` is used for ForeignKey relationships, while `prefetch_related()` is used for reverse and many-to-many relationships.

Database indexes are also added to frequently queried fields.

### Validation

Business validation is implemented at the serializer layer.

For example:

* Noise level cannot be negative.
* Noise level cannot exceed the configured maximum.
* High-noise events cannot be directly marked as resolved without review.

### Exception Handling

A centralized DRF exception handler provides a consistent API error structure.

Example:

```json
{
    "success": false,
    "error": {
        "detail": "No Airport matches the given query."
    }
}
```

### AI / LLM Integration

A separate service layer is used for LLM communication.

```text
API Request
     |
     v
AssetViewSet
     |
     v
AssetLLMService
     |
     v
LLM Provider
     |
     v
Generated Response
     |
     v
API Response
```

The service constructs controlled context from trusted asset data before sending the question to the model.

## API Documentation

Swagger UI:

```text
/api/docs/
```

ReDoc:

```text
/api/redoc/
```

OpenAPI schema:

```text
/api/schema/
```

## Example Noise Log

```json
{
    "airport": 1,
    "asset": 1,
    "noise_level": 85,
    "location": "Near Runway 12",
    "description": "High aircraft noise reported by nearby resident.",
    "recorded_at": "2026-09-16T04:03:43Z",
    "status": "OPEN"
}
```

The `reported_by` field is controlled by the server and is derived from the authenticated user rather than being accepted directly from the client.

## Running the Project

Clone the repository:

```bash
git clone https://github.com/gopianandakumar/aerosafe-noise-management-api.git
cd aerosafe-noise-management-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/api/docs/
```

## Security

The project excludes sensitive configuration from version control.

Examples include:

```text
.env
venv/
*.log
db.sqlite3
```

Environment-specific secrets should be supplied through environment variables rather than committed to the repository.

## Future Improvements

Potential production enhancements include:

* API versioning
* Rate limiting
* Redis caching
* Celery for asynchronous processing
* AWS deployment
* Centralized logging
* Monitoring and alerting
* Database high availability
* Circuit breakers for external dependencies
* Automated test coverage
* CI/CD pipeline
* Object-level permissions
* More advanced LLM/RAG capabilities

## Documentation

The repository also contains:

`AeroSafe_Architecture_Doc.pdf`

which provides additional architecture and project documentation.
