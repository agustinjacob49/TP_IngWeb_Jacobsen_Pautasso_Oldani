from django.shortcuts import render, redirect
from django.views.generic import (TemplateView)
from django.shortcuts import render
from .forms import UserRegisterForm

from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} ha sido creado')
            return redirect('home')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def privatePage(request):
    return render(request, 'page-private.html')