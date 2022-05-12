from django.db import models

class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, related_name="+")
    modified_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, related_name="+")

    class Meta:
        abstract = True

