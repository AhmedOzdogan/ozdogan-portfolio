from django.http import HttpResponse
from django.shortcuts import render
from .models import Menu

def index(request):
    return render(request, 'main/index.html')

def menu(request):
    return render(request, 'main/menu.html')

def menu_item(request, slug):
    return render(request, "main/menu_item.html", {"item_slug": slug})

def about(request):
    return HttpResponse('success')

def reservations(request):
    return HttpResponse('success')

def contact(request):
    return HttpResponse('success')
