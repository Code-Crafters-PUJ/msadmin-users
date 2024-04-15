from django.db import models
from Account import models as Account_models




class Module(models.Model):  # Subclass Model to define a Django model
    idModule = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)



class Permissions(models.Model):  # Subclass Model to define a Django model
    idPermissions = models.IntegerField(primary_key=True)
    idModule = models.ForeignKey(Module, on_delete=models.CASCADE)
    Operation = models.CharField(max_length=9, choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE')])
    idAccount = models.ForeignKey(
        Account_models.Account, on_delete=models.CASCADE)
    
