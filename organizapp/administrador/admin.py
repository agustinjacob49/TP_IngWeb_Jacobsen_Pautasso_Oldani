from django.contrib import admin
from .models import *
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "state")
    list_filter = ('name', "state")
    search_fields = ('name', "state")


class InvitationAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "accepted_event")
    list_filter = ('user', "event")
    search_fields = ('user', "event")


admin.site.register(Event, EventAdmin)
admin.site.register(Invitation, InvitationAdmin)
