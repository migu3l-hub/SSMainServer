from django.contrib.auth import authenticate, login as do_login, logout as do_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import FormularioLogin,Registro
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView
from .models import Servidor

# Create your views here.

def login(request):
    if request.method == "POST":
        nomusuario = request.POST.get("username")
        pwdenviada = request.POST.get("password")
        user = authenticate(request=request, username=nomusuario,password=pwdenviada)
        if user is not None:
            print(user.username)
            try:
                request.session['nombre'] = user.username
                do_login(request, user)
                return redirect('home')
            except Exception:
                return render(request, 'login.html',{"form": FormularioLogin, "errores": "Error al iniciar sesión"})
        else:
            return render(request, 'login.html', {"form": FormularioLogin, "errores": "Usuario y/o contraseña inválidos."})
    elif request.method == "GET":
        return render(request, "login.html", {"form": FormularioLogin})

def signup(request):
    if request.method == 'POST':
        form = Registro(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            do_login(request, user)
            return redirect('login')
        else:
            return render(request, 'registrarce.html',{"form": Registro, "errores":form.errors}) # MML se envian los errores del formulario
    else:
        form = Registro()
    return render(request, 'registrarce.html', {'form': form})


def home(request):
    if request.method == "GET":
        nom_usuario = request.session.get("usuario")
        try:
            usuario = User.objects.get(username=nom_usuario)
            servidores = Servidor.objects.filter(estado=True, usr=usuario)
            contexto = {"usuario": usuario, "servidores": servidores}
            return render(request, "servidores.html", contexto)
        except Exception:
            return render(request, "servidores.html", {"error": True})


################################### Administrador global ##########################################