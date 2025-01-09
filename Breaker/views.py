from django.shortcuts import render

def index(request):
    context = {
        'title': 'Welcome to My Django App',
        'description': 'This page is using Bootstrap for styling.',
        'items': ['Item 1', 'Item 2', 'Item 3', 'Item 4'],
    }
    return render(request, 'Breaker/index.html', context)
