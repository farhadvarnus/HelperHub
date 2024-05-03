from ..models import Category
from django import template

from ..models import Post
from django.db.models import Count, Q
from datetime import datetime, timedelta

from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.simple_tag
def title():
    return "وبلاگ جنگویی"


@register.inclusion_tag("blog/partials/categury_navbar.html")
def categury_navbar():
    return {"category": Category.objects.filter(statuses=True), }


@register.inclusion_tag("blog/partials/sidebar.html")
def popular_article():
    last_month = datetime.today() - timedelta(days=30)
    return {"articles": Post.objects.published().annotate(count=Count(
        'hits', filter=Q(articlehits__Created__gt=last_month))).order_by(
            '-count', 'Publish')[:2],
        'Title': "مقالات پر بازدید ماه"
    }


@register.inclusion_tag("blog/partials/sidebar.html")
def Hot_article():
    last_month = datetime.today() - timedelta(days=30)
    content_type_id = ContentType.objects.get(
        app_label='blog', model='article').id
    return {"articles": Post.objects.published().annotate(count=Count(
        'comments', filter=Q(comments__posted__gt=last_month) and Q(
            comments__content_type_id=content_type_id))).order_by(
            '-count', 'Publish')[:3],
            'Title': "مقالات پر بحث ماه"
            }


@register.inclusion_tag("blog/partials/sidebar.html")
def Rating_article():

    content_type_id = ContentType.objects.get(
        app_label='blog', model='article').id

    articles = Post.objects.published().annotate(count=Count(
        'ratings', filter=(Q(ratings__average__gt=content_type_id) & Q(
            ratings__count__gt=content_type_id))
    )).order_by('-ratings__count', '-ratings__average', '-Publish')[:3]

    return {
        "articles": articles,
        "Title": "مقالات پر امتیاز "
    }


@register.inclusion_tag('registration/partials/link.html')
def link(request, link_name, content, classes):
    return {
        'request': request,
        'link_name': link_name,
        'link': 'blog:{}'.format(link_name),
        'content': content,
        'classes': classes,
    }
