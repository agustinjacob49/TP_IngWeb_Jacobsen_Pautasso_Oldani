from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', home, name="home"),
    path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name="logout"),
    path('register/', register, name="register"),
    path('private-page/', login_required(privatePage), name="private_page")
] 
#+ statics(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)