from django.db import models
from users.models import User


# Create your models here.
class Poll(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=255, default='inactive')
    amount_of_questions = models.PositiveIntegerField(blank=True)
    picture = models.ImageField(null=True, upload_to='images/polls/')
    is_big_card = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User,
        null=True,
        related_name='polls',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

        class Meta:
            ordering = ['-date_created']


class Question(models.Model):
    title = models.TextField(db_index=True)
    amount_of_answers = models.PositiveIntegerField()
    poll = models.ForeignKey(
        Poll,
        null=True,
        related_name='questions',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.text


class Answer(models.Model):
    title = models.TextField(db_index=True)
    question = models.ForeignKey(
        'poll.Question',
        null=True,
        related_name='answers',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.answer_text
