#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input

# Automatically load sample data from backup.json
if [ -f "backup.json" ]; then
    echo "Loading sample data from backup.json..."
    python manage.py loaddata backup.json || true
fi

# Automatically create default admin superuser if it does not exist
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
Group.objects.get_or_create(name='Learners')
Group.objects.get_or_create(name='Admins')
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')
    print("Superuser created successfully: admin / admin12345")
EOF
