# Django Todo List Web App

A simple, elegant, and fully functional to-do list web application built with Django.

## Features

✅ **Create Todos** - Add new todo items with title and description
✅ **View Todos** - Browse all your todos in a clean, organized list
✅ **Edit Todos** - Update existing todo items
✅ **Delete Todos** - Remove completed or unwanted todos
✅ **Mark as Complete** - Toggle todo completion status with a single click
✅ **Responsive Design** - Works beautifully on desktop, tablet, and mobile
✅ **Admin Panel** - Manage todos through Django's admin interface
✅ **Bootstrap UI** - Modern, professional user interface

## Project Structure

```
DjangoTest/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── db.sqlite3                   # SQLite database (created after migration)
├── todoproject/                 # Main project folder
│   ├── __init__.py
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI application
└── todoapp/                     # Todo application folder
    ├── migrations/             # Database migrations
    ├── templates/              # HTML templates
    │   ├── base.html          # Base template
    │   └── todoapp/
    │       ├── todo_list.html           # Todo list view
    │       ├── todo_detail.html         # Todo detail view
    │       ├── todo_form.html           # Create/Edit form
    │       └── todo_confirm_delete.html # Delete confirmation
    ├── static/                 # Static files
    │   └── css/
    │       └── style.css       # Custom CSS styles
    ├── __init__.py
    ├── admin.py                # Admin configuration
    ├── apps.py                 # App configuration
    ├── forms.py                # Django forms
    ├── models.py               # Database models
    ├── tests.py                # Unit tests
    ├── urls.py                 # App URL configuration
    └── views.py                # View functions
```

## Installation

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 2. Clone or Download the Project
```bash
cd DjangoTest
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

This creates the SQLite database and applies all migrations.

### 5. Create a Superuser (Optional but Recommended)
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6. Start the Development Server
```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## Usage

### Web Interface
- **Home Page** (`/`): View all todos
- **Create Todo** (`/todo/create/`): Add a new todo
- **View Todo** (`/todo/<id>/`): See details of a specific todo
- **Edit Todo** (`/todo/<id>/edit/`): Update a todo
- **Delete Todo** (`/todo/<id>/delete/`): Remove a todo
- **Toggle Status**: Click the checkbox next to a todo to mark it as complete/incomplete

### Admin Panel
- Access at: `http://127.0.0.1:8000/admin/`
- Login with your superuser credentials
- Manage todos directly from the admin interface
- Filter todos by completion status and creation date
- Search todos by title or description

## Models

### Todo Model
```python
class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | List all todos |
| `/todo/create/` | GET, POST | Create a new todo |
| `/todo/<id>/` | GET | View todo details |
| `/todo/<id>/edit/` | GET, POST | Edit a todo |
| `/todo/<id>/delete/` | GET, POST | Delete a todo |
| `/todo/<id>/toggle/` | POST | Toggle todo completion |

## Testing

Run the test suite:
```bash
python manage.py test todoapp
```

## Database

The application uses SQLite by default for development. To switch to PostgreSQL or MySQL, modify the `DATABASES` setting in `todoproject/settings.py`.

### Backup Database
```bash
cp db.sqlite3 db.sqlite3.backup
```

### Reset Database
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Customization

### Adding More Fields to Todo
Edit `todoapp/models.py`:
```python
priority = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
due_date = models.DateTimeField(blank=True, null=True)
```

Then run:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Changing Styling
Edit `todoapp/static/css/style.css` to customize the appearance.

### Custom Themes
Modify the Bootstrap CDN link in `todoapp/templates/base.html` to use different Bootstrap themes.

## Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn todoproject.wsgi
```

### Using WhiteNoise (for static files)
```bash
pip install whitenoise
```

Update `todoproject/settings.py` middleware:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... rest of middleware
]
```

### Production Checklist
- [ ] Set `DEBUG = False` in settings.py
- [ ] Set a strong `SECRET_KEY`
- [ ] Configure allowed hosts
- [ ] Use environment variables for sensitive data
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Set up a production database (PostgreSQL recommended)
- [ ] Use HTTPS
- [ ] Configure CORS if needed

## Troubleshooting

### "No such table" error
```bash
python manage.py migrate
```

### Static files not loading
```bash
python manage.py collectstatic
```

### Port 8000 already in use
```bash
python manage.py runserver 8001
```

### Database locked
This is usually a SQLite issue. Try restarting the server.

## Future Enhancements

- 🔐 User authentication and per-user todos
- 📱 Mobile app (React Native/Flutter)
- 🔔 Email notifications for due todos
- 📊 Todo statistics and analytics
- 🏷️ Categories and tags
- 🔍 Advanced search and filtering
- 🌙 Dark mode
- 📅 Calendar view
- ⏰ Reminders and notifications
- 🤖 AI-powered smart suggestions

## License

MIT License - Feel free to use this project for personal and commercial purposes.

## Support

For issues or questions, please create an issue or contact the development team.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Happy Todo-ing!** 🎯
