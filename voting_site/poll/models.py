# from datetime import datetime, date
from django.utils import timezone
from django.db import models
from users.models import User


class Poll(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    start_at = models.DateField()
    end_at = models.DateField()
    amount_of_questions = models.PositiveIntegerField(blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to='images/polls/')
    is_big_card = models.BooleanField(default=False)
    creator = models.ForeignKey(
        User,
        null=True,
        related_name='polls',
        on_delete=models.CASCADE
    )

    @property
    def is_active(self):
        self.now = timezone.now()
        return self.start_at <= self.now <= self.end_at

    @property
    def questions(self):
        return self.question_set.all()

    class Meta:
        ordering = ['-created_at']

    # def save():
    #
    #     super().save()

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.TextField(db_index=True)
    # amount_of_choices = models.PositiveSmallIntegerField(null=True)
    poll = models.ForeignKey(
        Poll,
        null=True,
        related_name='questions',
        on_delete=models.CASCADE
    )

    @property
    def choices(self):
        return self.choice_set.all()

    @property
    def amount_of_choices(self):
        return self.choices.count()

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


class Answer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        'users.User',
        null=True,
        related_name='users',
        on_delete=models.CASCADE

    )
    choice = models.ForeignKey(
        'poll.Choice',
        null=True,
        related_name='choices',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '{}-{}'.format(self.user.username, self.choice.title)


class Account(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def has_items(self):
        return self.items.exists()

    @property
    def items_count(self):
        return self.items.count()
