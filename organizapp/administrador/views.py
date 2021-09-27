from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.shortcuts import render
import secrets
from django.contrib import messages

from django.template.context_processors import csrf
from django.views.generic import DetailView

from .forms import *
from .models import *
from django.core.mail import send_mail
import datetime
from django.utils import timezone

# import ipdb; ipdb.set_trace(); para debuguear, n->avanzo, c->hasta el final
# Create your views here.
def home(request):
    # limito los usuarios y eventos a solo 10, proximamente hacer una vista con todos los eventos
    # y todas los usuarios
    users = User.objects.all().order_by('-id')[0:10]
    events = Event.objects.all().order_by('-id')[0:10]

    # Si existe un link
    if request.GET.get('event_link_name'):
        token = request.GET.get('event_link_name')
        token = token[38:]

        event = Event.objects.get(event_link=token)
        if not Invitation.objects.filter(user=request.user, event=event).exists():
            new_invitation = Invitation.objects.create(user=request.user, event=event, accepted_event=True)
            new_invitation.save()
            messages.success(request, "Te has unido a este evento con éxito.")
            return render(request, 'event.html', {'event': event})
        else:
            messages.error(request, "Ya estas unido a este evento")
            return render(request, 'event.html', {'event': event})

    return render(request, 'home.html', {'users': users,
                                         'events': events})


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
        redirect('home.html')

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


def AddEvent(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event_instance = form.save(commit=False)
            """ le paso el usuario que creo el evento y genero un token para el link"""
            event_instance.owner_id = request.user.id
            event_instance.event_link = secrets.token_hex(30)
            event_instance.save()

            """ Creo la invitacion del organizador """
            new_invitation = Invitation.objects.create(user=request.user, event=event_instance, accepted_event = True)
            new_invitation.save()

            messages.success(request, ('Evento creado con exito!'))

            return HttpResponseRedirect(reverse('event', kwargs={'token': event_instance.event_link}))
        else:
            messages.error(request, 'Hay errores en el formulario')

    form = EventForm()
    return render(request, 'new-event.html', {'form': form})


def EventView(request, token):
    event = Event.objects.get(event_link=token)
    return render(request, 'event.html', {'event': event})


def DeleteEvent(request, token):
    event = Event.objects.get(event_link=token)
    event.delete()
    messages.success(request, "Evento borrado con éxito")
    return redirect('home')


# Desde el perfil, clickeando sobre los iconos de estado de aceptacion puedo darle de baja o alta a la invitacion
def EventDown(request, pk, token):
    event = Event.objects.get(event_link=token)
    invitation = Invitation.objects.get(user_id=pk, event_id=event.id)
    invitation.accepted_event = False
    invitation.save()
    invitations = Invitation.objects.filter(user_id=pk)
    return render(request, 'profile.html', {'invitations': invitations})


def EventUp(request, pk, token):
    event = Event.objects.get(event_link=token)
    invitation = Invitation.objects.get(user_id=pk, event_id=event.id)
    invitation.accepted_event = True
    invitation.save()
    invitations = Invitation.objects.filter(user_id=pk)
    return render(request, 'profile.html', {'invitations': invitations})


def Profile(request, pk):
    user = User.objects.get(id=pk)
    invitations = Invitation.objects.filter(user_id=pk)[:10]
    return render(request, 'profile.html', {'invitations': invitations,
                                            'user': user})


def event_listing(request):
    event_list = Invitation.objects.filter(user_id=request.user.id)
    # Con paginator puedo dividir de a 10 registros
    paginator = Paginator(event_list, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'invitations-by-profile.html', {'page_obj': page_obj,
                                                            'invitations': paginator.object_list})


def CreateInvitationByLink(request, pk, link):
    event = Event.objects.get(event_link=link)
    if len(event.list_invitation) < event.max_guests:
        new_invitation = Invitation.objects.create(user_id=pk, event_event_link=link)
        new_invitation.accepted_event = True
        new_invitation.save()
        return render(request, 'event.html', {'event': event})
    else:
        messages.error(request, 'El evento alcanzó la cantidad máxima de invitados')
        return render(request, 'event.html', {'event': event})