from django.db import models
from users.models import User


# Create your models here.
class Poll(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    amount_of_questions = models.PositiveIntegerField(blank=True)
    picture = models.ImageField(null=True, upload_to='images/polls/')
    is_big_card = models.BooleanField(default=False)
    creator = models.ForeignKey(
        User,
        null=True,
        related_name='polls',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.TextField(db_index=True)
    amount_of_answers = models.PositiveSmallIntegerField()
    poll = models.ForeignKey(
        Poll,
        null=True,
        related_name='questions',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Answer(models.Model):
    title = models.TextField(db_index=True)
    question = models.ForeignKey(
        'poll.Question',
        null=True,
        related_name='answers',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Choice(models.Model):
    title = models.TextField(db_index=True)
    made_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(
        'poll.Question',
        null=True,
        related_name='choices',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

class Account(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    owner = models.OneToOneField(
        User,
        related_name='accounts',
        on_delete=models.CASCADE
    )

    @property
    def items_count(self):
        return self.items.count()
