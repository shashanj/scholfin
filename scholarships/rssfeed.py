from django.contrib.syndication.views import Feed
from scholarships.models import *
from django.utils import feedgenerator
from django.utils.feedgenerator import Atom1Feed

class LatestEntriesFeed(Feed):

    feed_type = feedgenerator.Rss201rev2Feed
    title = 'Latest Scholarship'
    link = '/rssfeed/'
    description = 'Scholarship'

    
    def items(self):
        return scholarship.objects.order_by('-timestamp')[:50]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.about

    def item_pubdate(self, item):
        return item.timestamp

class AtomSiteNewsFeed(LatestEntriesFeed):
    feed_type = Atom1Feed
    subtitle = LatestEntriesFeed.items
    author_name = 'Scholfin'
    def item_updateddate(self, item):
     	return item.timestamp