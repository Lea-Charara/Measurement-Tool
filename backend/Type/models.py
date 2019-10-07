# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Type(models.Model):
    typename = models.TextField()
    

    def __str__(self):
        return self.typename
