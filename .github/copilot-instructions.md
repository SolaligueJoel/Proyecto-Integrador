# AI Agent Instructions for Meli App Project

## Project Overview
This is a Flask-based web application for visualizing rental property data from Mercado Libre (Meli). The app provides user authentication and rental property visualization through pie charts.

## Authentication Implementation
- User model (`src/clases/users.py`) implements `UserMixin` for Flask-Login compatibility
- Password hashing using Werkzeug's `generate_password_hash` with SHA-256
- User validation functions for username and email uniqueness
- Session management through Flask-Login with custom user loader
- Required fields: username, email, password, and timestamp

## Data Integration & APIs
### Mercado Libre Integration
- API endpoint: `https://api.mercadolibre.com/sites/MLA/search`
- Category filter: `MLA1459` (Rental Properties)
- Fetches up to 50 properties per request
- Currency filtering for ARS (Argentine Peso)
- Implementation in `src/clases/localidad.py:fetch()`

## Architecture & Key Components

### Core Components
- **Web Server**: Flask application (`app.py`)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login implementation
- **Frontend**: HTML templates with CSS and JavaScript

### Key Directories
- `/src/clases/`: Core business logic classes
  - `users.py`: User authentication and management
  - `localidad.py`: Location and property data handling
- `/templates/`: Jinja2 templates for views
- `/static/`: Frontend assets (CSS, JS, images)
- `/src/configuracion/`: Configuration management

## Development Workflows

### Environment Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Database initialization happens automatically on first run through `app.py`

### Configuration
- Configuration is managed through `src/configuracion/config.ini`
- Database and server settings are loaded via `config.py`

## Key Patterns & Conventions

### Database Operations
- All database models extend SQLAlchemy's `db.Model`
- Schema creation functions are defined in model classes (see `users.create_schema()`)
- Database file path is configured in `config.ini`

### Authentication Flow
- Login required for protected routes (using `@login_required` decorator)
- User session management through `flask_login.LoginManager`
- Registration flow starts at `/signup` endpoint

### Frontend Integration
- Base template: `templates/base.html`
- Chart rendering: `templates/grafico.html` using Matplotlib
- Form validation: `static/js/formulario.js`

## Common Operations
- Adding new routes: Add to `app.py` with appropriate template
- User management: Extend `src/clases/users.py`
- Property data: Modify `src/clases/localidad.py`
- Styling changes: Update `static/css/style.css` and `home.css`

## Integration Points
- Mercado Libre API integration (for property data)
- Matplotlib for chart generation
- SQLite database (local storage)

## Database Schema
### Users Table
- `id`: Integer, Primary Key, Autoincrement
- `user_name`: String(20), Unique
- `email`: String(50)
- `password`: String(50), Hashed
- `time`: String (timestamp)

### Localidad (Property) Table
- `id`: Integer, Primary Key, Autoincrement
- `location`: String
- `price_min`: Integer
- `price_max`: Integer
- `time`: String (timestamp)

## Chart Generation
1. Data Fetching:
   - Fetches property data from Meli API
   - Filters by currency (ARS)
   - Processes price ranges
2. Visualization:
   - Uses Matplotlib for pie chart generation
   - Chart rendered in `templates/grafico.html`
   - Dynamic updates based on user filters

## Configuration Management
### File Structure
- Primary config: `src/configuracion/config.ini`
  ```ini
  [db]
  database=localidad.db
  schema=schema.sql
  [server]
  host=127.0.0.1
  port=5000
  ```
- Config parsing: `src/configuracion/config.py`
- Database path configured relative to script location
- Server settings for local development

## Testing & Debugging
The application logs can be monitored through Flask's built-in logging system. Database errors are caught and traced in route handlers.

## Error Handling Patterns
- Database operations wrapped in try-except blocks
- API integration errors logged with traceback
- Form validation errors displayed via flash messages
- Session management errors redirect to login