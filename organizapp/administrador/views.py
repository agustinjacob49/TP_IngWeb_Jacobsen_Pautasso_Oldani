import datetime
import hashlib
from random import random

from django.contrib.messages import success
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.generic import (TemplateView)
from django.shortcuts import render
from .forms import UserRegisterForm
import secrets
from django.contrib import messages

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

from django.template.context_processors import csrf
from .forms import *
from .models import *
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone

# Create your views here.
def home(request):
    users = UserProfile.objects.all()
    return render(request, 'home.html', {'users': users})


def register_user(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # guardar el usuario en la base de datos si es válido
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = secrets.token_hex(20)
            activation_key = salt+email
            key_expires = datetime.datetime.today() + datetime.timedelta(1)

            #Obtener el nombre de usuario
            user=User.objects.get(username=username)

            # Crear el perfil del usuario
            new_profile = UserProfile(user=user, activation_key=activation_key,
                key_expires=key_expires)
            new_profile.save()

            # Enviar un email de confirmación
            email_subject = 'Confirmacion de cuenta Organizat'
            email_body = "Hola %s, Gracias por registrarte. Para activar tu cuenta da clíck en este link en menos de 24 horas: http://organizat.herokuapp.com/accounts/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'myemail@example.com',
                [email], fail_silently=False)
            messages.success(request, "Cuenta registrada con exito! Revisa tu casilla de correos para confirmar la cuenta")
            return redirect('home')
        else:
            messages.error(request, form.errors)
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})


def register_confirm(request, activation_key):
    # Verifica que el usuario ya está logeado
    if request.user and request.user.is_authenticated:
        HttpResponseRedirect('home')

    # Verifica que el token de activación sea válido y sino retorna un 404
    user_profile = UserProfile.objects.get(activation_key=activation_key)

    # verifica si el token de activación ha expirado y si es así renderiza el html de registro expirado
    if user_profile.key_expires < timezone.now():
        messages.success(request,
                             "El token ha expirado! Intenta registrarte nuevamente (recuerde que tiene 24hs. para confirmar la cuenta).")
        return redirect('home.html')
    # Si el token no ha expirado, se activa el usuario y se muestra el html de confirmación
    user = user_profile.user
    user.is_active = True
    user.save()
    messages.success(request,
                         "La cuenta se ha activado con exito.")
    return render(request, 'home.html')


def privatePage(request):
    return render(request, 'page-private.html')