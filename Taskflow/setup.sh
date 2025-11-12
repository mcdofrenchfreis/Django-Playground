#!/bin/bash
# Setup script for Django Todo App on Linux/Mac

echo "============================================"
echo "  Django Todo List App - Setup"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "[1/5] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed successfully"

echo ""
echo "[2/5] Running migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Error: Failed to run migrations"
    exit 1
fi
echo "✓ Migrations applied successfully"

echo ""
echo "[3/5] Collecting static files..."
python manage.py collectstatic --noinput > /dev/null 2>&1
echo "✓ Static files collected"

echo ""
echo "[4/5] Creating superuser..."
echo "Please enter superuser credentials:"
python manage.py createsuperuser
if [ $? -ne 0 ]; then
    echo "Error: Failed to create superuser"
    exit 1
fi
echo "✓ Superuser created successfully"

echo ""
echo "[5/5] Setup complete!"
echo ""
echo "============================================"
echo "  Next Steps:"
echo "============================================"
echo ""
echo "To start the development server, run:"
echo "  python manage.py runserver"
echo ""
echo "Then open your browser and go to:"
echo "  http://127.0.0.1:8000/"
echo ""
echo "Admin panel (after creating superuser):"
echo "  http://127.0.0.1:8000/admin/"
echo ""
echo "============================================"
