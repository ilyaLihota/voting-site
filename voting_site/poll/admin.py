from django.contrib import admin
from poll.models import Poll, Question, Choice, Answer


admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
