from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


from .models import UserFileModel
from .file_read import create_students

User = get_user_model()


@receiver(post_save, sender=UserFileModel)
def create_or_modify_students_by_file(sender, instance, created, **kwargs):
    print("post save signals in user")
    if created:
        create_students(file=instance.file)
    return instance

 