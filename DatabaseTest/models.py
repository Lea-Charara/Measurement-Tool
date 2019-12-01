from django.db import models
from Database.models import Database
from Test.models import Test

# Create your models here.
class DatabaseTest(models.Model):
    Test_id = models.ForeignKey(Test, on_delete = models.CASCADE)
    DB_id = models.ForeignKey(Database, on_delete = models.CASCADE)
    query = models.TextField()
    Test_Duration = models.DecimalField(max_digits=5,decimal_places=2,default = 0)
    Nb_of_done = models.IntegerField(default=0)
    def __str__(self):
        return self.query