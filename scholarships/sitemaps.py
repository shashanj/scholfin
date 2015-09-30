from django.contrib.sitemaps import Sitemap
import re
from scholarships.models import *

class ScholarshipSitemap(Sitemap):
	changefreq="weekly"
	priority = 0.5

	def items(self):
		return scholarship.objects.all()
	def lastmod(self,item):
		return item.timestamp