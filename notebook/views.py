from django.shortcuts import render
from .models import Note

def notes_list(request):
    notes_list = Note.objects.all()
    return render(request, 'notebook.html', {'notes_list':notes_list})

# Create your views here.
