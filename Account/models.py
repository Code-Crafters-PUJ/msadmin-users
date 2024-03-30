from django.db import models


class role(models.Model):
    idrole = models.AutoField(primary_key=True)
    role = models.CharField(max_length=50)


# Create your models here.
class Account(models.Model):
    idcuenta = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    cedula = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now=True)
    role = models.ForeignKey(role, on_delete=models.CASCADE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_anonymous = False
    is_authenticated = True
