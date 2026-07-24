from django.contrib.auth.models import Group

def admin_status(request):
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return {'is_admin': False}
    is_admin = (
        request.user.is_staff or 
        request.user.is_superuser or 
        request.user.groups.filter(name="Admins").exists()
    )
    return {'is_admin': is_admin}
