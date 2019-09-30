from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Poll(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    amount_of_questions = models.PositiveIntegerField()
    # picture = models.ImageField(null=True, upload_to='img/')
    # owner = models.ForeignKey(
    #     User,
    #     null=True,
    #     related_name='polls',
    #     on_delete=models.SET_NULL
    # )

    class Meta:
        pass

    def __str__(self):
        return self.title
