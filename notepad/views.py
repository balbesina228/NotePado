from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render


def index(request):
    return HttpResponse('Sample text 1.')


def page_not_found(request, exception):
    return HttpResponseNotFound('Page not found!')
