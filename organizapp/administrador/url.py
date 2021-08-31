from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', home, name="home"),
    path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name="logout"),
    path('register/', register_user, name="register"),
    path('private-page/', login_required(privatePage), name="private_page"),
    path('accounts/confirm/<str:activation_key>/', register_confirm, name="activation"),

    path('profile/<int:pk>', login_required(Profile), name="profile"),

    path('add-event/', login_required(AddEvent), name="add_event"),
    path('event/<str:token>/', login_required(EventView), name="event"),
]
#+ statics(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)