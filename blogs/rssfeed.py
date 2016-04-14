# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.syndication.views import Feed
from blogs.models import *
from django.utils import feedgenerator
from django.utils.feedgenerator import Atom1Feed

class LatestEntriesFeed(Feed):

    feed_type = feedgenerator.Rss201rev2Feed
    title = 'Latest Blog'
    link = '/rssfeed/'
    description = 'Blog'

    
    def items(self):
        return Blog.objects.order_by('-posted')[:50]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_pubdate(self, item):
        return item.posted

class AtomSiteNewsFeed(LatestEntriesFeed):
    feed_type = Atom1Feed
    subtitle = LatestEntriesFeed.items
    author_name = 'Scholfin'
    def item_updateddate(self, item):
     	return item.posted