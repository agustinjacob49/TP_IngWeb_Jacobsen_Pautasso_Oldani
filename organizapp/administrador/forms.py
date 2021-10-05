from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Event, Task
from datetime import date


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields } # Quito las ayudas para crear una pass

    # modificamos el método save() así podemos definir  user.is_active a False la primera vez que se registra
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False
            user.save()

        return user

    #clean email field
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('email duplicado')


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date_event_start', 'date_event_end',
                  'location', 'state', 'max_guests', 'visibility']

        widgets = {'date_event_start': forms.DateInput(
                    format=('%Y-%m-%dT%H:%M'),
                    attrs={'type': 'datetime-local'
                           }),
                    'date_event_end': forms.DateInput(
                    format=('%Y-%m-%dT%H:%M'),
                    attrs={'type': 'datetime-local'
                           })
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        self.fields["date_event_start"].initial = date.today()
        self.fields["date_event_end"].initial = date.today()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['user', 'title', 'description', 'status',
                  'cost']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

        self.fields["cost"].initial = 0
        self.fields["cost"].required = False


