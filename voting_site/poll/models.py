from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Poll(models.Model):
    created = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User,
        null=True,
        related_name='polls',
        on_delete=models.SET_NULL
    )

    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # status = models.PositiveIntegerField()
    amount_of_questions = models.PositiveIntegerField()

    def __str__(self):
        return self.title
