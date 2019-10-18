from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View
from django.views.decorators.http import require_GET, require_POST
from django.urls import reverse

from .models import *
from .forms import PollForm, QuestionForm, ChoiceForm


def pagination(polls, page_number):
    amount_of_polls_on_page = 5
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


def account(request, user_id=None):
    user = get_object_or_404(User, id=user_id)
    user_polls = Poll.objects.filter(creator_id=user_id)
    context = {'user': user, 'user_polls': user_polls}

    return render(request, 'poll/account.html', context)


class PollCreate(View):
    def get(self, request, user_id):
        creator = get_object_or_404(User, id=user_id)
        form = PollForm()
        context={'user': creator, 'form': form}

        return render(request, 'poll/poll_create_form.html', context)

    def post(self, request, user_id):
        creator = get_object_or_404(User, id=user_id)
        form = PollForm(request.POST)
        print('request:', request.POST)
        if form.is_valid():
            new_poll = form.save(commit=False)
            new_poll.picture = request.POST['picture']
            new_poll.creator = creator
            new_poll.save()
            return redirect(reverse('poll_detail_url', kwargs={'id': new_poll.id}))

        context={'user': creator, 'form': form}
        return render(request, 'poll/poll_create_form.html', context)


class PollDetail(View):
    def get(self, request, id=None):
        poll = get_object_or_404(Poll, id=id)
        context = {'poll': poll}

        return render(request, 'poll/poll_detail.html', context)


class PollUpdate(View):
    def get(self, request, poll_id):
        poll = get_object_or_404(Poll, pk=poll_id)
        bound_form = PollForm(instance=poll)
        context = {'form': bound_form, 'poll': poll}

        return render(request, 'poll/poll_update_form.html', context)

    def post(self, request, poll_id):
        poll = get_object_or_404(Poll, pk=poll_id)
        bound_form = PollForm(request.POST, instance=poll)

        if bound_form.is_valid():
            updated_poll = bound_form.save(commit=False)
            updated_poll.picture = request.POST['picture']
            updated_poll.save()
            return redirect(reverse('account_url', kwargs={'user_id': updated_poll.creator_id}))

        context = {'form': bound_form, 'poll': poll}
        return render(request, 'poll/poll_update_form.html', context)


class PollDelete(View):
    def get(self, request, poll_id):
        poll = get_object_or_404(Poll, pk=poll_id)
        context = {'poll': poll}

        return render(request, 'poll/poll_delete_form.html', context)

    def post(self, request, poll_id):
        poll = get_object_or_404(Poll, pk=poll_id)
        user = get_object_or_404(User, id=poll.creator_id)
        poll.delete()

        return redirect(reverse('account_url', kwargs={'user_id': user.id}))


class QuestionCreate(View):
    def get_poll(self, poll_id):
        return get_object_or_404(Poll, id=poll_id)

    def get(self, request, poll_id):
        poll = self.get_poll(poll_id)
        form = QuestionForm()
        context = {'poll': poll, 'form': form}

        return render(request, 'poll/question_create_form.html', context)

    def post(self, request, poll_id):
        poll = self.get_poll(poll_id)
        bound_form = QuestionForm(request.POST)

        if bound_form.is_valid():
            new_question = bound_form.save(commit=False)
            new_question.poll = poll
            new_question.save()
            return redirect(reverse('poll_detail_url', kwargs={'id': poll.id}))

        context = {'poll': poll, 'form': bound_form}
        return render(request, 'poll/question_create_form.html', context)


class QuestionDetail(View):
    def get(self, request, question_id=None):
        question = get_object_or_404(Question, pk=question_id)
        context = {'question': question}

        return render(request, 'poll/question_detail.html', context)


class QuestionUpdate(View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        bound_form = QuestionForm(instance=question)
        context = {'question': question, 'form': bound_form}

        return render(request, 'poll/question_update_form.html', context)

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        bound_form = QuestionForm(request.POST, instance=question)

        if bound_form.is_valid():
            updated_question = bound_form.save()

            return redirect(reverse('poll_detail_url', kwargs={'id': updated_question.poll_id}))

        context = {'question': question, 'form': bound_form}
        return render(request, 'poll/question_update_form.html', context)


class QuestionDelete(View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        context = {'question': question}

        return render(request, 'poll/question_delete_form.html', context)

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        poll = get_object_or_404(Poll, id=question.poll_id)
        question.delete()

        return redirect(reverse('poll_detail_url', kwargs={'id': poll.id}))


class ChoiceCreate(View):
    def get_question(self, question_id):
        return get_object_or_404(Question, id=question_id)

    def get(self, request, question_id):
        question = self.get_question(question_id)
        form = ChoiceForm()
        context = {'question': question, 'form': form}

        return render(request, 'poll/choice_create_form.html', context)

    def post(self, request, question_id):
        question = self.get_question(question_id)
        bound_form = ChoiceForm(request.POST)

        if bound_form.is_valid():
            new_choice = bound_form.save(commit=False)
            new_choice.question = question
            new_choice.save()
            return redirect(reverse('question_detail_url', kwargs={'question_id': question.id}))

        context = {'question': question, 'form': bound_form}
        return render(request, 'poll/choice_create_form.html', context)


class ChoiceUpdate(View):
    def get(self, request, choice_id):
        choice = get_object_or_404(Choice, id=choice_id)
        bound_form = ChoiceForm(instance=choice)
        context = {'choice': choice, 'form': bound_form}

        return render(request, 'poll/choice_update_form.html', context)

    def post(self, request, choice_id):
        choice = get_object_or_404(Choice, id=choice_id)
        bound_form = ChoiceForm(request.POST, instance=choice)

        if bound_form.is_valid():
            updated_choice = bound_form.save()
            return redirect(reverse('question_detail_url', kwargs={
                'question_id': choice.question_id
            }))

        context = {'choice': choice, 'form': bound_form}
        return render(request, 'poll/choice_update_form.html', context)


class ChoiceDelete(View):
    def get(self, request, choice_id):
        choice = get_object_or_404(Choice, id=choice_id)
        context = {'choice': choice}

        return render(request, 'poll/choice_delete_form.html', context)

    def post(self, request, choice_id):
        choice = get_object_or_404(Choice, id=choice_id)
        question = get_object_or_404(Question, id=choice.question_id)
        choice.delete()

        return redirect(reverse('question_detail_url', kwargs={
            'question_id': question.id
        }))


class Result(View):
    def get(self, request, poll_id):
        poll = get_object_or_404(Poll, id=poll_id)
        questions = Question.objects.filter(poll_id=poll.id)
        choices = {}

        for question in questions:
            list_choice = question.choices.all()
            choices[question] = list_choice

        context = {'poll': poll, 'choices': choices}
        return render(request, 'poll/result.html', context)


class Voted(View):
    def get(self, request):
        user = request.user
        answers = Answer.objects.filter(user_id=user.id)
        voted_polls = {}

        for answer in answers:
            choice = answer.choice
            question = choice.question
            poll = question.poll

            if poll not in voted_polls:
                voted_polls[poll] = answer.created_at

        context = {'polls': voted_polls}
        return render(request, 'poll/voted_polls.html', context)


class TakePoll(View):
    def get(self, request, poll_id):
        poll = get_object_or_404(Poll, id=poll_id)
        questions = Question.objects.filter(poll_id=poll_id)
        context = {}

        for question in questions:
            choices = Choice.objects.filter(question_id=question.id)
            context[question.id] = [question, choices]

        return render(request, 'poll/take_poll_form.html', context={
            'context': context,
            'poll': poll
        })

    def post(self, request, poll_id):
        user = request.user
        user_choice = request.POST['radio_btn']
        instance_choice = get_object_or_404(Choice, title=user_choice)

        if not Answer.objects.filter(user=user, choice=instance_choice).exists():
            answer = Answer.objects.create(user=user, choice=instance_choice)
            answer.save()

        return redirect(reverse('take_poll_url', kwargs={'poll_id': poll_id}))
