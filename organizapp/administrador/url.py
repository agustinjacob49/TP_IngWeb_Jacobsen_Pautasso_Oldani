from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', home, name="home"),
    path('login/', CustomLoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name="logout"),
    path('register/', register_user, name="register"),
    path('accounts/confirm/<str:activation_key>/', register_confirm, name="activation"),

    path('profile/<int:pk>/', login_required(Profile), name="profile"),
    path('profile/events/', login_required(event_listing), name="profile_invitations"),

    path('add-event/', login_required(AddEvent), name="add_event"),
    path('delete-event/<str:token>/', login_required(DeleteEvent), name="delete_event"),
    path('event/<str:token>/', login_required(EventView), name="event"),
    path('event/<int:pk>/<str:link>/', login_required(CreateInvitationByLink), name="event_by_link"),
    path('event-down/<int:pk>/<str:token>/', login_required(EventDown), name="event_down"),
    path('event-up/<int:pk>/<str:token>/', login_required(EventUp), name="event_up"),
    
    path('activate-event/<int:pk>/', login_required(ActivateEvent), name="activate_event"),
    path('hide-event/<int:pk>/', login_required(HideEvent), name="hide_event"),
    
    path('invitation-down/<int:pk>/<str:token>/', login_required(InvitationDown), name="invitation_down"),
    path('invitation-up/<int:pk>/<str:token>/', login_required(InvitationUp), name="invitation_up"),
    path('invite-users/<str:token>/', login_required(InviteUsers.as_view()), name="invite_user"),
    path('invite-user/<int:pk>/<str:token>/', login_required(send_mail_user), name="send_mail_user"),
    path('add_task/<str:token>/', login_required(AddTask), name="add_task"),
    path('event/update-task/<str:token>/<int:task_pk>/', login_required(UpdateTask), name="update_task"),
    path('update-task-status/<int:pk>/<str:status>', login_required(UpdateStatusTask), name="update-task-status"),
    path('robots.txt/',TemplateView.as_view(template_name="robots.txt", content_type="text/plain"))
]
#+ statics(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)