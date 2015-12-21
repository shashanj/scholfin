from django.db import models

class Institute(models.Model):
    name = models.CharField(primary_key= True ,max_length=150)
    short_name = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
