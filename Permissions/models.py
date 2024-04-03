from django.db import models
from Account import models as Account_models


class Operation(models.Model):  # Subclass Model to define a Django model
    idOperation = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)


class Modulo(models.Model):  # Subclass Model to define a Django model
    idModule = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)


class Permissions(models.Model):  # Subclass Model to define a Django model
    idPermissions = models.IntegerField(primary_key=True)
    idModule = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    idOperation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    idAccount = models.ForeignKey(
        Account_models.Account, on_delete=models.CASCADE)
    
