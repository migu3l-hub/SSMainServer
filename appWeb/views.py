from django.shortcuts import render
from django.contrib.auth import authenticate, login as do_login, logout as do_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from .models import *
from threading import Timer
from appWeb import decoradores
#from axes.decorators import axes_dispatch
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView

# Create your views here.

def login(request):
    if request.method == "POST":
        nomusuario = request.POST.get("username")
        pwdenviada = request.POST.get("password")
        user = authenticate(request=request, username=nomusuario,password=pwdenviada)
        if user is not None:
            try:
                request.session['nombre'] = user.username
                do_login(request, user)
                return redirect('token_global')
            except Exception as error:
                return render(request, 'global/login_global.html',{"form": admin_form, "errores": "Error al iniciar sesión"})
        else:
            return render(request, 'global/login_global.html', {"form": admin_form, "errores": "Usuario y/o contraseña inválidos."})
    elif request.method == "GET":
        return render(request, "global/login_global.html", {"form": admin_form})


################################### Administrador global ##########################################