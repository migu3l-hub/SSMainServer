from django.shortcuts import redirect
from django.utils.decorators import method_decorator

def no_esta_logueado(vista):
    def interna(request, pk=""):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('global:index')
        if request.user.is_authenticated:
            return redirect('home')
        return vista(request)
    return interna


def class_view_decorator(function_decorator):
    def deco(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View
    return deco


def no_es_usuario(vista):
    def interna(request, pk=""):
        if request.user.is_superuser:
            return redirect('global:index')
        return vista(request)
    return interna


def no_es_admin(vista):
    def interna(request, pk=""): # ESTO ES NECESARIO PARA QUE TRABAJEN LAS VISTAS QUE ENVIAN COSAS COMO UNA CLAVE PRIMARIA
        if not request.user.is_superuser:
            return redirect('home')
        return vista(request)
    return interna
