from django.db import models
from Type.models import Type
# Create your models here.

class Database(models.Model):
    name = models.TextField()
    host = models.TextField()
    port = models. IntegerField()
    username = models.TextField()
    password = models.TextField()
    dbtype = models.ForeignKey(Type, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

    def getall(self):
        return self.self._meta.model.objects.all()