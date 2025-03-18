from django.db import models

from authentication.models import User
from helpers.models import TrackingModel


# Create your models here.
class Todo(TrackingModel):
    """
        A simple Todos model.
    """
    title = models.CharField(max_length=255)
    desc = models.TextField()
    is_complete = models.BooleanField(default=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
