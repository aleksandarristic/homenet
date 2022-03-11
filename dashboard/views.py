from django.shortcuts import render

from dashboard.models import MenuURL


def index(request):
    context = {
        'menu_items': MenuURL.objects.filter(active=True)
    }
    template = 'dashboard/index.html'
    return render(request, template, context)
