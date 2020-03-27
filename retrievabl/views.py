from django.shortcuts import render


def index(request):
    return render(request, 'retrievabl/index.html')


def search(request):
    return render(request, 'retrievabl/base_page.html')


def mission(request):
    return render(request, 'retrievabl/our_mission.html')