from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Menu
from .forms import MessagesForm, ReservationsForm

def index(request):
    return render(request, 'main/index.html')

def menu(request):
    return render(request, 'main/menu.html')

def menu_item(request, slug):
    return render(request, "main/menu_item.html", {"item_slug": slug})

def about(request):
    return HttpResponse('success')

def reservations(request):
    form = ReservationsForm()  #(no POST handling)
    return render(request, 'main/reservations.html', {'form': form})

def contact(request):
    form = MessagesForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(status=204)
    return render(request, 'main/contact.html', {'form': form})
