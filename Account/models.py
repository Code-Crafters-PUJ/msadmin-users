from django.db import models


class role(models.Model):
    idrole = models.AutoField(primary_key=True)
    role_descripction = models.CharField(max_length=50)






# Create your models here.
class Account(models.Model):
    idcuenta = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_card = models.CharField(max_length=10, unique=True)
    last_login = models.DateTimeField(auto_now=True)
    connected = models.BooleanField(default=False)
    role = models.ForeignKey(role, on_delete=models.CASCADE)


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    activity = models.CharField(max_length=45)
    date = models.DateTimeField(auto_now=True)


class Credentials(models.Model):
    idcuenta = models.ForeignKey(Account, on_delete=models.CASCADE)
    email = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_anonymous = False
    is_authenticated = True
