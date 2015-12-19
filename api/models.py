from django.db import models

class Institute(models.Model):
    name = models.CharField(primary_key= True ,max_length=50)
    short_name = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name
