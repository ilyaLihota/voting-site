from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View
from django.urls import reverse

from .models import *
from .forms import PollForm
from .utils import ObjectDetailMixin


def pagination(polls, page_number):
    amount_of_polls_on_page = 6
    paginator = Paginator(polls, amount_of_polls_on_page, orphans=amount_of_polls_on_page)
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

    return context


def search(request):
    query = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)
    polls = Poll.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query)
    )
    return render(request, 'poll/main.html', context=pagination(polls, page_number))


def polls_list(request):
    page_number = request.GET.get('page', 1)
    polls = Poll.objects.all()

    return render(request, 'poll/main.html', context=pagination(polls, page_number))


def poll_create(request):
    if request.method == 'GET':
        form = PollForm()
        return render(request, 'poll/poll_create_form.html', context={
            'form': form,
        })
    elif request.method == 'POST':
        bound_form = PollForm(request.POST)
        if bound_form.is_valid():
            new_poll = bound_form.save()
            return redirect(new_poll)
        return render(request, 'poll/poll_create_form.html', context={
            'form': bound_form,
        })


class PollDetail(ObjectDetailMixin, View):
    model = Poll
    template = 'poll/poll_detail.html'


class PollUpdate(View):
    def get(self, request, poll_id):
        poll = get_object_or_404(Poll, pk=poll_id)
        bound_form = PollForm(instance=poll)
        return render(request, 'poll/poll_update_form.html', context={
            'form': bound_form,
            'poll': poll
        })

    def post(self, request, poll_id):
        poll = get_object_or_404(Poll, pk=poll_id)
        bound_form = PollForm(request.POST, instance=poll)

        if bound_form.is_valid():
            updated_poll = bound_form.save()
            return redirect(updated_poll)
        return render(request, 'poll/poll_update_form.html', context={
            'form': bound_form,
            'poll': poll
        })


class PollDelete(View):
    def get(self, request, poll_id):
        poll = get_object_or_404(Poll, pk=poll_id)
        return render(request, 'poll/poll_delete_form.html', context={
            'poll': poll
        })

    def post(self, request, poll_id):
        poll = get_object_or_404(Poll, pk=poll_id)
        poll.delete()
        return redirect('/')


def questions_create(request):
    if request.method == 'GET':
        form = QuestionForm()
        return render(
            request,
            'poll/question_create_form.html',
            context={'form': form}
        )
    elif request.method == 'POST':
        bound_form = QuestionForm(request.POST)
        if bound_form.is_valid():
            new_question = bound_form.save()
            return redirect(new_question)
        return render(request, 'poll/question_create_form.html', context={
            'form': bound_form
        })


def account(request, id=None):
    user_polls = Poll.objects.filter(creator_id=id)

    # print('id:', id)
    # print(user_polls)

    return render(request, 'poll/account.html', context={
        'user_polls': user_polls
    })
