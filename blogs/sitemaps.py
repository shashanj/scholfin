# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.sitemaps import Sitemap
import re
from blogs.models import *

class BlogSitemap(Sitemap):
	changefreq="weekly"
	priority = 1

	def items(self):
		return Blog.objects.all()
	def lastmod(self,item):
		return item.posted