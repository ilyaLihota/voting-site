from django.shortcuts import render
from django.http import HttpResponse


def main_page(request):
    return render(request, 'poll/polls_cards.html')
