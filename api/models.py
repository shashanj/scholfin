from django.db import models

class Institute(models.Model):
	institute_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
