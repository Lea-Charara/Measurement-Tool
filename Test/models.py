from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.TextField()
    description = models.TextField()
    repetition = models.IntegerField()
    timeout = models.IntegerField()
    Progress = models.IntegerField(default=0) 
    Status = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name