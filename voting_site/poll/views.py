from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View
from django.views.decorators.http import require_GET, require_POST
from django.urls import reverse

from .models import *
from .forms import PollForm
from .forms import BaseQuestionFormset, QuestionFormset
# from .utils import ObjectDetailMixin


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


def poll_create(request, user_id):
    creator = get_object_or_404(User, id=user_id)

    if request.method == 'GET':
        form = PollForm()

    elif request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            new_poll = form.save(commit=False)
            new_poll.creator = creator
            new_poll.save()
            return redirect(reverse('poll_detail_url', kwargs={'id': new_poll.id}))

    context={'user': creator, 'form': form}
    return render(request, 'poll/poll_create_form.html', context)


class PollDetail(View):
    def get(self, request, id=None):
        poll = get_object_or_404(Poll, id=id)
        return render(request, 'poll/poll_detail.html', context={
            'poll': poll
        })


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
            return redirect(reverse('account_url', kwargs={'user_id': updated_poll.creator_id}))

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
        user = get_object_or_404(User, id=poll.creator_id)
        poll.delete()

        return redirect(reverse('account_url', kwargs={'user_id': user.id}))


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


class QuestionDetail(View):
    def get(self, request, question_id=None):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'poll/question_detail.html', context={
            'question': question
        })


def account(request, user_id=None):
    user = get_object_or_404(User, id=user_id)
    user_polls = Poll.objects.filter(creator_id=user_id)
    context = {'user': user, 'user_polls': user_polls}

    return render(request, 'poll/account.html', context)


def manage_question(request, poll_id):
    """Edit question and their choices for a single poll."""

    poll = get_object_or_404(Poll, id=poll_id)
    Question
    if request.method == 'POST':
        formset = QuestionFormset(request.POST, instance=poll)
        if formset.is_valid():
            formset.save()
            return redirect('poll_detail_url', poll_id=poll.id)
    else:
        formset = QuestionFormset(instance=poll)

    return render(request, 'poll/question_choices_create.html', context={
        'poll': poll,
        'question_formset': formset
    })
