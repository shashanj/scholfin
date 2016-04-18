# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models import permalink
from ckeditor.fields import RichTextField

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField()
    #slug = models.SlugField(prepopulate_from=('title',))
    body = RichTextField()
    desc = models.CharField(max_length=200, blank=True)
    posted = models.DateField(db_index=True, auto_now_add=True)
    category = models.ForeignKey('blogs.Category',blank=True)
    class Meta:
        ordering  = ['-posted']
    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_blog_post', None, { 'slug': self.slug })

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    image = models.ImageField(blank=True)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_blog_category', None, { 'slug': self.slug })


