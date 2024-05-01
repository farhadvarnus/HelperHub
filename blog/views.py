from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.utils import timezone
from django.contrib.auth import authenticate, login
# Create your views here.


def home_blog(request, **kwargs):
    posts = Post.objects.filter(
        published_date__lte=timezone.now(), status=1)
    if kwargs.get('cat_name') != None:
        posts = posts.filter(category__name=kwargs['cat_name'])
    elif kwargs.get("author_username") != None:
        posts = posts.filter(author__username=kwargs["author_username"])
    elif kwargs.get('tag_name') != None:
        posts = posts.filter(tags__name__in=[kwargs['tag_name']])
    posts = Paginator(posts, 3)
    try:
        page_number = request.GET.get("page")
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)
    context = {"posts": posts}
    return render(request, "blog/home.html", context)


def single_blog(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now(), status=1)
    post = get_object_or_404(posts, pk=pid)
    post.counted_view += 1
    post.save()

    nex = False
    next = 404
    prev_post = 404
    next_post = 404

    for i, po in enumerate(posts):
        if nex:
            next = po.id
            break
        if po.id == post.id:
            if i == 0:
                prev = 404
            if i != 0:
                prev = temp
            nex = True

        temp = po.id
    if next != 404:
        next_post = get_object_or_404(posts, pk=next)
    if prev != 404:
        prev_post = get_object_or_404(posts, pk=prev)
    context = {"post": post, 'posts': posts,
               "next": next_post, "prev": prev_post}
    return render(request, "blog/single.html", context)


def search_blog(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now(), status=1)
    if request.method == "GET":
        posts = posts.filter(content__contains=request.GET.get("s"))

    context = {"posts": posts}
    return render(request, "blog/home.html", context)
