from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Category, Likes
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
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
    posts = Paginator(posts, 6)
    try:
        page_number = request.GET.get("page")
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)
    context = {"posts": posts}
    return render(request, "blog/home.html", context)


def single_blog(request, pid):
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
    query = request.GET.get('s')  # دریافت پارامتر جستجو از آدرس
    categories = Category.objects.filter(
        name__icontains=query)  # جستجو در نام دسته بندی
    posts = Post.objects.filter(
        title__icontains=query) | Post.objects.filter(
        author__username__icontains=query)
    # جستجو در عنوان پست و نام نویسنده
    context = {
        'categories': categories,
        'posts': posts,
        'query': query,
    }
    return render(request, "blog/home.html", context)


def like_blog(request, pid):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR,
                             'you must be sign in for like any courses!!!')
        return HttpResponseRedirect(reverse('blog:single', args=[pid]))
    user = request.user.id
    post = Post.objects.get(id=pid)
    current_likes = post.like
    liked = Likes.objects.filter(user=user, post=post).count()
    if not liked:
        liked = Likes.objects.create(user=request.user, post=post)
        current_likes += 1
    else:
        liked = Likes.objects.filter(user=user, post=post).delete()
        current_likes -= 1
    post.like = current_likes
    post.save()
    return HttpResponseRedirect(reverse('blog:single', args=[pid]))


def liked_courses_blog(request):
    user = request.user.id
    liked_post = Likes.objects.filter(user_id=user).values('post_id')
    print(liked_post)
    all_post = []
    for post in liked_post:
        all_post += (Post.objects.filter(id=post.get('post_id')))

    context = {"posts": all_post}
    return render(request, "blog/home.html", context)
