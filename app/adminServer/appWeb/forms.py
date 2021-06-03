from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User
from appWeb import api
from appWeb.models import Servidor


class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):  # es el metodo que ejecuta toda clase de python lo redifinimos
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


class Registro(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(Registro, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = "form-control"
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password2'].widget.attrs['class'] = "form-control"
        self.fields['password2'].widget.attrs[
            'placeholder'] = 'vuelva a introducir contraseña'  # MML el campo password solo se manipula desde aqui

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'nombre de usuario',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'nombre real',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'apellido',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'correo electrónico',
                }
            ),
        }


class AdminForm(forms.ModelForm):
    # MML verificacion de Contraseña
    pwd2 = forms.CharField(label='Contraseña de confirmación', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese de nuevo la contraseña',
            'id': 'pwd2',
            'required': 'required',
        }
    ))

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de usuario',
            'password': 'Contraseña del administrador',
            'first_name': 'Nombre real del administrador',
            'last_name': 'Apellidos del administrador',
            'email': 'Correo del administrador',
        }

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre de usuario',
                    'id': 'usr'
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la contraseña del administrador',
                    'id': 'pwd'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre del administrador',
                    'id': 'nombres'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese los apellidos del administrador',
                    'id': 'apellidos'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el correo del administrador',
                    'id': 'correo'
                }
            ),
        }

    def clean_pwd2(self):  # MML Hacemos la verificacion de si la contraeña coincide
        pwd1 = self.cleaned_data['password']
        pwd2 = self.cleaned_data['pwd2']
        if pwd1 != pwd2:
            raise forms.ValidationError('Las contraseñas no coinciden')  # Este es el error que esta en forms.error
        return pwd2

    def save(self, commit=True):
        user = super().save(commit=False)  # MML se redefine la forma en que se guarda la contraseña
        pwd_hash = api.hashear_contrasena(self.cleaned_data['password'])
        user.password = pwd_hash
        if commit:
            user.save()
        return user


class ServerForm(forms.ModelForm):
    class Meta:
        model = Servidor
        fields = ('desc_srv', 'ip_srv', 'puerto', 'usr', 'estado', 'puerto_tty')
        label = {
            'desc_srv': 'Descrićión del servidor',
            'ip_srv': 'IP del servidor',
            'puerto': 'Puerto del servidor',
            'usr': 'Administrador del servidor',
            'estado': 'Estado del servidor',
            'puerto_tty': 'Puerto Terminal',
        }
        widgets = {
            'desc_srv': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Pequeña descripcion',
                }
            ),
            'ip_srv': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'IP del servidor',
                }
            ),
            'puerto': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Puerto del servidor',
                }
            ),
            'puerto_tty': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Puerto de la terminal del servidor',
                }
            ),
            'usr': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'estado': forms.CheckboxInput(),
        }
