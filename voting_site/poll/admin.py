from django.contrib import admin
from poll.models import Poll, Question, Answer

# Register your models here.
admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Answer)
