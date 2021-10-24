from django.db.models.query_utils import Q
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.shortcuts import render
import secrets
from django.contrib import messages
from django.template.context_processors import csrf
from django.views.generic import DetailView, ListView

from .forms import *
from .models import *
from django.core.mail import send_mail
import datetime
from datetime import date, datetime
from django.utils import timezone
from purl import URL
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

# import ipdb; ipdb.set_trace(); para debuguear, n->avanzo, c->hasta el final
# Create your views here.
def home(request):
    # limito los usuarios y eventos a solo 10, proximamente hacer una vista con todos los eventos
    # y todas los usuarios
    users = User.objects.all().order_by('-id')[0:10]
    events = Event.objects.all().order_by('-id')[0:10]

    # Si existe un link
    if request.GET.get('event_link_name'):
        token = URL(request.GET.get('event_link_name'))
        token = token.path_segments()[1]

        event = Event.objects.get(event_link=token)
        if not Invitation.objects.filter(user=request.user, event=event).exists():
            if len(event.list_invitation_accepted) < event.max_guests:
                new_invitation = Invitation.objects.create(user=request.user, event=event, accepted_event=True)
                new_invitation.save()
                messages.success(request, "Te has unido a este evento con éxito.")
                return render(request, 'event.html', {'event': event})
            else:
                messages.error(request, 'El evento alcanzó la cantidad máxima de invitados')
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
            if event_instance.date_event_start > event_instance.date_event_end:
                messages.error(request, 'La fecha de inicio del evento no es valida (debe ser anterior a la fecha de finalizacion)')
                return render(request, 'new-event.html', {'form': form})
            elif event_instance.date_event_start.date() < datetime.now().date():
                messages.error(request, 'La fecha de inicio del evento no es valida (debe ser mayor a la fecha y hora del dia de hoy)')
                return render(request, 'new-event.html', {'form': form})
            else:
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
    if request.GET.get('event_link_name'):
        token = URL(request.GET.get('event_link_name'))
        token = token.path_segments()[1]

        event = Event.objects.get(event_link=token)
        if not Invitation.objects.filter(user=request.user, event=event).exists():
            if len(event.list_invitation_accepted) < event.max_guests:
                new_invitation = Invitation.objects.create(user=request.user, event=event, accepted_event=True)
                new_invitation.save()
                messages.success(request, "Te has unido a este evento con éxito.")
            else:
                messages.error(request, 'El evento alcanzó la cantidad máxima de invitados')
        else:
            messages.error(request, "Ya estas unido a este evento")        

    if event.list_invitation.filter(user = request.user).first() is not None:
        isGuest = True
    else:
        isGuest = False

    return render(request, 'event.html', {'event': event, 'isGuest': isGuest })


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
        new_invitation.accepted_event = False
        new_invitation.save()
        return render(request, 'event.html', {'event': event})
    else:
        messages.error(request, 'El evento alcanzó la cantidad máxima de invitados')
        return render(request, 'event.html', {'event': event})


def InvitationDown(request, pk, token):
    invitation = Invitation.objects.get(id=pk)
    invitation.accepted_event = False
    invitation.save()
    event = Event.objects.get(event_link = token)
    return render(request, 'event.html', {'event': event})


def InvitationUp(request, pk, token):
    invitation = Invitation.objects.get(id=pk)
    invitation.accepted_event = True
    invitation.save()
    event = Event.objects.get(event_link=token)
    return render(request, 'event.html', {'event': event})

def UpdateStatusTask(request, pk, status):
    task = Task.objects.get(id=pk)
    task.status = status
    task.save()
    event = Event.objects.get(event_link = task.event.event_link)

    if event.list_invitation.filter(user = request.user).first() is not None:
        isGuest = True
    else:
        isGuest = False

    return render(request, 'event.html', {'event': event, 'isGuest':isGuest})


class CustomAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Por favor, chequear si la cuenta se encuentra validada o ingrese correctamente el %(username)s y password. Ambos campos pueden ser sensibles a mayusculas y minusculas "
        ),
        'inactive': _("This account is inactive."),
    }


class CustomLoginView(LoginView):
    authentication_form = CustomAuthForm


class InviteUsers(ListView):
    ## event = Event.objects.get(event_link='hola')
    model = User
    template_name = 'invite_users.html'
    queryset = User.objects.filter(is_active = True)
    context_object_name = 'user'
    ordering = ['-id']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(InviteUsers, self).get_context_data(**kwargs)
        context["event"] = Event.objects.get(event_link = self.kwargs.get('token'))

        return context

    def get_queryset(self): 
        queryset = super(InviteUsers, self).get_queryset()
        ## Me traigo la lista de usuarios que ya aceptaron.
        list_accepted = Event.objects.get(event_link = self.kwargs.get('token')).list_users_accepted

        ## Los excluyo de mi queryset segun la pk.
        queryset = queryset.exclude(pk__in=[user.pk for user in list_accepted])
        
        query = self.request.GET.get('find_user')
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query)
            )

        return queryset


def send_mail_user(request, pk, token):
    event = Event.objects.get(event_link=token)
    user = User.objects.get(id=pk)
    email_subject = 'Has recibido una invitación a un evento!'
    email_body = "Hola " + user.username + ", el usuario " + event.owner.username + " te ha invintado a participar de su evento. \n"+\
                 "Haz click en el siguiente enlace para acceder : " + "http://organizat.herokuapp.com/event/" + event.event_link

    send_mail(email_subject, email_body, 'myemail@example.com',
              [user.email], fail_silently=False)
    messages.success(request, ('Usuario ' + user.username + ' ha sido invitado con éxito'))
    return redirect(reverse('invite_user', kwargs={ 'token': event.event_link }))


def AddTask(request, token):
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task_instance = form.save(commit=False)
            if task_instance.user:
                task_instance.status = 'POR HACER ASIGNADA'
            else:
                task_instance.status = 'POR HACER NO ASIGNADA'
            task_instance.event = Event.objects.get(event_link = token)
            task_instance.save()

            messages.success(request, ('Tarea creada con exito!'))
            
            # Si se le asignó un usuario, le envio un mail
            if task_instance.user:
                user = task_instance.user
                event = task_instance.event
                
                email_subject = 'Te han asignado una tarea en un evento!'
                email_body = "Hola " + user.username + ", el usuario " + event.owner.username + " te ha asignado una tarea de su evento. \n"+\
                            "Haz click en el siguiente enlace para acceder al evento: " + "http://organizat.herokuapp.com/event/" + event.event_link

                send_mail(email_subject, email_body, 'myemail@example.com',[user.email], fail_silently=False)

            return HttpResponseRedirect(reverse('event', kwargs={'token': token}))
        else:
            messages.error(request, 'Hay errores en el formulario')

    form = TaskForm()
    event = Event.objects.get(event_link=token)
    return render(request, 'new-task.html', {'form': form,
                                             'event': event,
                                             'update': False})


def UpdateTask(request, token, task_pk):
    instance = Task.objects.get(id=task_pk)
    form = TaskForm(request.POST or None, instance=instance)
    hasError = False
    if request.method == 'POST':
        if form.is_valid():
            ## Si la tarea tiene estado POR HACER NO ASIGNADA y seteamos un usuario. Cambiamos el estado a por hacer asignada.
            if instance.status == '':
                instance.status = 'POR HACER NO ASIGNADA'
                
            if instance.status == 'POR HACER NO ASIGNADA' and form.instance.user:
                form.instance.status = 'POR HACER ASIGNADA'
            else:
                ## Si la tarea esta en POR HACER ASIGNADA y quitamos el usuario -> Cambiamos el estado a POR HACER NO ASIGNADA.
                if instance.status == 'POR HACER ASIGNADA' and not form.instance.user:
                    form.instance.status = 'POR HACER NO ASIGNADA'
            
            ## Si la tarea esta en POR HACER ASIGNADA y quitamos el usuario -> Cambiamos el estado a POR HACER NO ASIGNADA.
            if instance.status == 'EN PROGRESO' or instance.status == 'REALIZADA' and not form.instance.user:
                messages.error(request, 'El estado de la tarea es "EN PROGRESO" o "REALIZADA" y no se permite desasignar usuario')
                hasError = True

            if form.instance.user and instance.status == 'POR HACER NO ASIGNADA':
                messages.error(request, 'El estado de la tarea es "POR HACER NO ASIGNADA" no permite asignar un usuario')
                hasError = True
            
            if not hasError:
                form.save()
            return HttpResponseRedirect(reverse('event', kwargs={'token': token}))
                
        else:
            messages.error(request, form.errors)

    event = Event.objects.get(event_link=token)
    assigned_user = None
    if instance.user:
        assigned_user = User.objects.get(id=instance.user.id)
    
    context = {
        'form': form,
        'event': event,
        'update': True,
        'assigned_user': assigned_user
    }
    return render(request, 'new-task.html', context)