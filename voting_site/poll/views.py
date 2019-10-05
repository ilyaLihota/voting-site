from django.shortcuts import render, get_object_or_404

from .models import Poll
from django.core.paginator import Paginator


# Create your views here.
# def search(request):
#     q = request.GET.get('q')
#     page_num =
#
#     return render(request, 'poll/search.html', context={
#         pass
#     })


def polls_list(request):
    amount_of_polls_on_page = 4
    polls = Poll.objects.all()
    paginator = Paginator(polls, amount_of_polls_on_page, orphans=4)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
    }

    return render(request, 'poll/main.html', context=context)


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
