from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Главная страница')

def group_posts(request):
    return HttpResponse('Страница с постами')

def post_detail(request, pk):
    return HttpResponse(f'Пост номер {pk}')