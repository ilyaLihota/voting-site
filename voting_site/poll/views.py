from django.shortcuts import render, get_object_or_404

from .models import Poll

# Create your views here.
def polls_list(request):
    polls = Poll.objects.all()
    return render(request, 'poll/main.html', context={'polls': polls})


def poll_detail(request, id=None):
    poll = get_object_or_404(Poll, id=id)
    context = {
        'id': poll.id,
        'title': poll.title,
        'description': poll.description,
        'date_created': poll.date_created,
        'start_time': poll.start_time,
        'end_time': poll.end_time,
        'status': poll.status,
        'amount_of_questions': poll.amount_of_questions,
        'picture': poll.picture,
        'owner': poll.owner,
    }
    return render(request, 'poll/poll_detail.html', context)
