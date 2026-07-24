from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from .models import Post2, Achievement

@receiver(pre_delete, sender=Post2)
def log_post2_delete(sender, instance, **kwargs):
    Achievement.objects.create(
        original_model='Post2',
        original_pk=instance.pk,
        title=getattr(instance, 'title', None),
        text=getattr(instance, 'text', None),
        image_path=(instance.image.url if getattr(instance, 'image', None) else None),
        action='deleted',
        changed_at=timezone.now(),
        changed_by=getattr(instance, '_deleted_by', None)  # custom tracking
    )

from django.db.models.signals import pre_save
from .models import Post2

@receiver(pre_save, sender=Post2)
def log_post2_edit(sender, instance, **kwargs):
    if instance.pk:  # Only if updating an existing record
        try:
            old_instance = Post2.objects.get(pk=instance.pk)
        except Post2.DoesNotExist:
            return
        # Save old version in Achievements
        Achievement.objects.create(
            original_model='Post2',
            original_pk=old_instance.pk,
            title=getattr(old_instance, 'title', None),
            text=getattr(old_instance, 'text', None),
            image_path=(old_instance.image.url if getattr(old_instance, 'image', None) else None),
            action='edited',
            changed_at=timezone.now(),
            changed_by=getattr(instance, '_edited_by', None)  # custom tracking
        )
