from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Poll, Account


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, id=None):
        obj = get_object_or_404(self.model, id=id)
        return render(request, self.template, context={
            self.model.__name__.lower(): obj
        })
