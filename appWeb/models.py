
from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class Servidor(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    desc_srv = models.CharField(max_length=16, blank=False, null=False)
    ip_srv = models.CharField(max_length=12, blank=False, null=False)
    puerto = models.IntegerField(blank=False, null=False)
    estado = models.BooleanField("Activo/Inactivo", default=True)
    usr_srv = models.CharField("Usuario servidor", max_length=25, blank=False, null=False, default=" ")
    pwd_srv = models.CharField("Contraseña Servidor", max_length=50, blank=False, null=False, default="0")
    usr = models.ForeignKey(User, on_delete=models.CASCADE)
    puerto_tty = models.CharField("Puerto terminal", max_length=5, blank=False, null=False, default="0")
    llave = models.CharField(max_length=50, blank=False, null=False, default="0")