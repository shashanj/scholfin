from django.contrib.sitemaps import Sitemap

from scholarships.models import *

class ScholarshipSitemap(Sitemap):
	changefreq="weekly"
	priority = 0.5

	def items(self):
		return scholarship.objects.all()