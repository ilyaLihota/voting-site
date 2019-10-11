from django.contrib import admin
from poll.models import Poll, Question, Choice, Answer, Account

# Register your models here.
admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(Account)
