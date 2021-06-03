from django.contrib.auth import authenticate, login as do_login, logout as do_logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from axes.decorators import axes_dispatch
from django.views.decorators.csrf import csrf_exempt
from . import decorators, api
from .forms import FormularioLogin, Registro, ServerForm, AdminForm
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from .models import Servidor
from random import randint


# Create your views here.
from adminServer import settings


@axes_dispatch
@decorators.no_esta_logueado
def login(request):
    if request.method == "POST":  # GIG POST significa que el usuario envio datos que debemos procesar
        nomusuario = request.POST.get("username")
        pwdenviada = request.POST.get("password")
        user = authenticate(request=request, username=nomusuario, password=pwdenviada)
        if user is not None:
            try:
                do_login(request, user)  # MML guarda el id del usuario en la sesion almacenado en {{ user }} y aqui se accede como request.session.get("user")
                #request.session.set_expiry(settings.EXPIRY_TIME)
                return redirect('home')
            except Exception:
                return render(request, 'login.html', {"form": FormularioLogin, "errores": "Error al iniciar sesión"})
        else:
            return render(request, 'login.html',{"form": FormularioLogin, "errores": "Usuario y/o contraseña inválidos."})
    elif request.method == "GET":
        return render(request, "login.html", {"form": FormularioLogin})


def signup(request):
    if request.method == 'POST':
        form = Registro(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'registrarce.html',{"form": Registro, "errores": form.errors})  # MML se envian los errores del formulario
    else:
        form = Registro()
    return render(request, 'registrarce.html', {'form': form})


@decorators.no_es_usuario
def home(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            try:
                servidores = Servidor.objects.filter(estado=True, usr=request.user)
                for servidor in servidores:
                    if api.servidor_activo(servidor.ip_srv,servidor.puerto_tty):
                        servidor.puerto_activotty = True
                    if api.servidor_activo(servidor.ip_srv, servidor.puerto):
                        servidor.puerto_activorest = True
                contexto = {"servidores": servidores}
                return render(request, "servidores.html", contexto)
            except Exception:
                return render(request, "servidores.html",{"error": True})  # MML los errores aparecen tan solo si hay un error en la plantilla


@csrf_exempt # Como la peticion de ajax es por post necesita el csrf entonces lo debemos deshabilitar
def monitoreo(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            servidor = Servidor.objects.get(estado= True,id = pk, usr=request.user)
            return render(request, 'monitoreo.html', {"servidor":servidor})
    elif request.method == "POST":
        data = {}
        try:
            action = request.POST.get('action') # Se tiene que poner entre parentecis ya funciona
            if action == 'obtener_datos_monitor':
                servidor = Servidor.objects.get(estado=True, id=pk, usr=request.user)
                data = {'y': api.obtener_cpu(api.solicitar_datos_srv(servidor))}
            elif action == 'obtener_datos_memoria':
                servidor = Servidor.objects.get(estado=True, id=pk, usr=request.user)
                data = {'y': api.obtener_memoria(api.solicitar_datos_srv(servidor))}
            elif action == 'obtener_datos_disco':
                servidor = Servidor.objects.get(estado=True, id=pk, usr=request.user)
                data = {'y': api.obtener_disco(api.solicitar_datos_srv(servidor))}
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)



def logout(request):
    do_logout(request)
    return redirect("login")


# Vistas administrador global ##############
@axes_dispatch
@decorators.no_esta_logueado
def login_global(request):
    if request.method == 'POST':
        nomuser = request.POST.get("username")
        conuser = request.POST.get("password")
        user = authenticate(request, username=nomuser, password=conuser)
        if user is not None:
            if user.is_superuser:
                try:
                    do_login(request, user)
                    return redirect('global:index')
                except Exception:
                     return render(request, 'global/login_global.html',
                                  {"form": FormularioLogin, "errores": "Error al iniciar sesión"})
            else:
                return render(request, 'login.html',
                              {"form": FormularioLogin, "errores": "Usuario por favor inicia sesion aquí."})
        else:
            return render(request, 'global/login_global.html',
                          {"form": FormularioLogin, "errores": "Usuario y/o contraseña inválidos."})
    elif request.method == "GET":
        return render(request, "global/login_global.html", {"form": FormularioLogin})


@decorators.no_es_admin
def inicio(request):
    if request.method == "GET":
        return render(request, 'global/index.html')


@decorators.class_view_decorator(decorators.no_es_admin)
class ListarAdministrador(ListView):
    model = User
    template_name = 'global/listar_admin.html'
    context_object_name = 'admins'
    queryset = User.objects.filter(is_superuser=False)


@decorators.class_view_decorator(decorators.no_es_admin)
class ActualizarAdministrador(UpdateView):
    model = User
    form_class = AdminForm
    template_name = 'global/crear_admin.html'
    success_url = reverse_lazy('global:listar_admin')


@decorators.class_view_decorator(decorators.no_es_admin)
class CrearAdministrador(CreateView):
    model = User
    form_class = AdminForm
    template_name = 'global/crear_admin.html'
    success_url = reverse_lazy('global:listar_admin')


@decorators.class_view_decorator(decorators.no_es_admin)
class EliminarAdministrador(DeleteView):
    model = User
    success_url = reverse_lazy('global:listar_admin')


@decorators.class_view_decorator(decorators.no_es_admin)
class CrearServer(CreateView):
    model = Servidor
    form_class = ServerForm
    template_name = 'global/crear_server.html'
    success_url = reverse_lazy('global:listar_server')


@decorators.class_view_decorator(decorators.no_es_admin)
class ListarServidor(ListView):  # MML esta incompleto
    model = Servidor
    template_name = 'global/listar_server.html'
    context_object_name = 'servers'
    queryset = Servidor.objects.all()


@decorators.class_view_decorator(decorators.no_es_admin)
class ActualizarServidor(UpdateView):
    model = Servidor
    form_class = ServerForm
    template_name = 'global/server.html'
    success_url = reverse_lazy('global:listar_server')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servers'] = Servidor.objects.filter(estado=True)
        return context


@decorators.class_view_decorator(decorators.no_es_admin)
class EliminarServidor(DeleteView):
    model = Servidor
    success_url = reverse_lazy('global:listar_server')

