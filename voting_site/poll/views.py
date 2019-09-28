from django.shortcuts import render
from .models import Poll

# Create your views here.
def polls_list(request):
    polls = Poll.objects.all()
    return render(request, 'poll/index.html', context={'polls': polls})
