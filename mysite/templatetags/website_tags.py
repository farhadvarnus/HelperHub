from django import template
from blog.models import Post
from django.utils import timezone
register = template.Library()


@register.inclusion_tag('mysite/most-recently-post.html')
def most_recently_post():
    posts = Post.objects.filter(
        published_date__lte=timezone.now(), status=1).order_by("published_date")[:6]
    return {'posts': posts}
