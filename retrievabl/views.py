from django.shortcuts import render
from django.conf import settings


def index(request):
    return render(request, 'retrievabl/index.html')


def search(request):
    return render(request, 'retrievabl/search.html')


def mission(request):
    return render(request, 'retrievabl/our_mission.html')


def genNegLM(request):
    f = open(settings.NEG_WORDS, 'r')
    nw = f.read()
    return render(request, 'retrievabl/search/html')
