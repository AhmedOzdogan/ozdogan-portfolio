from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

def menu(request):
    return render(request, 'main/menu.html')

def menu_item(request, item_id):
    return render(request, 'main/menu_item.html', {'item_id': item_id})
