from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

# Create your models here.

STATES_EVENTO = [
    ('activo', 'ACTIVO'),
    ('finalizado', 'FINALIZADO'),
    ('oculto', 'OCULTO'),
    ('suspendido', 'SUSPENDIDO')
]

STATES_EVENTO_USUARIO = [
    ('activo', 'ACTIVO'),
    ('oculto', 'OCULTO')
]

STATES_TAREAS = [
    ('REALIZADA', 'REALIZADA'),
    ('POR HACER ASIGNADA', 'POR HACER ASIGNADA'),
    ('EN PROGRESO', 'EN PROGRESO'),
    ('POR HACER NO ASIGNADA', 'POR HACER NO ASIGNADA')
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=255, blank=True)
    key_expires = models.DateTimeField(default=date.today)
    date_start = models.DateTimeField(default=date.today)
    date_end = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=10, choices=STATES_EVENTO, verbose_name='Estado', null=True)

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
    state = models.CharField(max_length=10, choices=STATES_EVENTO_USUARIO, verbose_name='Estado', null=True)
    max_guests = models.IntegerField(verbose_name='Capacidad máxima de invitados')
    visibility = models.CharField(max_length=14, choices=VISIBILITIES, verbose_name='Visibilidad')

    @property
    def list_invitation(self):
        return Invitation.objects.filter(event=self)

    @property
    def list_invitation_accepted(self):
        return Invitation.objects.filter(event=self, accepted_event=True)

    @property
    def list_tasks(self):
        return Task.objects.filter(event=self)

    @property
    def total_amount(self):
        total = 0
        for i in self.list_tasks:
            total += i.cost

        return round((total/len(self.list_invitation_accepted)), 1)

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


class Task(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Encargado")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Evento")
    title = models.CharField(max_length=50, blank = False, null = False, verbose_name = 'Titulo')
    description = models.CharField(max_length=255, blank = False, null = False, verbose_name = 'Descripcion')
    status = models.CharField(choices = STATES_TAREAS, blank = False, null = False, max_length=22, verbose_name='Estado de la tarea')
    cost = models.FloatField(default = 0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'