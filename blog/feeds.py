from django.contrib.syndication.views import Feed
from django.db.models.base import Model
from django.urls import reverse
from django.utils.safestring import SafeText
from .models import Post
from django.utils import timezone


class LatestEntriesFeed(Feed):
    title = "blog newest posts"
    link = '/rss/feed'
    description = 'bes blog for free learning'

    def items(self):
        return Post.objects.filter(
            published_date__lte=timezone.now(), status=1)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:100]
