from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

# Create your models here.

STATES = [
    ('activo', 'ACTIVO'),
    ('inactivo', 'INACTIVO'),
    ('oculto', 'OCULTO'),
    ('suspendido', 'SUSPENDIDO')
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=255, blank=True)
    key_expires = models.DateTimeField(default=date.today)
    date_start = models.DateTimeField(default=date.today)
    date_end = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=10, choices=STATES, verbose_name='Estado', null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


VISIBILITIES = [
    ('publico', 'PÚBLICO '),
    ('privado', 'PRIVADO')
]


class Event(models.Model):
    name = models.CharField(max_length=40, blank=True, null=False, verbose_name='Nombre')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Organizador")
    description = models.TextField(max_length=255, blank=True, null=False, verbose_name='Descripcion')
    date_event_start = models.DateTimeField(default=datetime.today(), verbose_name='Fecha de alta del evento')
    date_event_end = models.DateTimeField(default=datetime.today(), verbose_name='Fecha de baja del evento')
    location = models.CharField(max_length=255, blank=True, null=False, verbose_name='Ubicación')
    event_link = models.URLField(max_length=200, verbose_name='Link')
    state = models.CharField(max_length=10, choices=STATES, verbose_name='Estado', null=True)
    max_guests = models.IntegerField(verbose_name='Capacidad máxima de invitados')
    visibility = models.CharField(max_length=14, choices=VISIBILITIES, verbose_name='Visibilidad')

    @property
    def list_invitation(self):
        return Invitation.objects.filter(event=self)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'


class Invitation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Integrate")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Evento")
    accepted_event = models.BooleanField(default=False, verbose_name="Aceptado")

    def __str__(self):
        return self.event.name + ' - ' + self.user.username

    class Meta:
        verbose_name = 'Invitacion'
        verbose_name_plural = 'Invitaciones'