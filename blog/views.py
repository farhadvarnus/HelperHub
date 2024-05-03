from django.shortcuts import render, get_object_or_404
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView

from dashboard.forms import UserForms
from accounts.models import User
from blog.models import Post, Category
from dashboard.mixins import (
    FieldsMixin,
    FormMixin,
    SuperUserAccessMixin,
    AuthorsAccessMixin, )
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


class Detail_list(DetailView):

    def get_object(self):
        # میاد هرچی ک مال اسلاگه رو میگیره = هرمقداری اسلاگ داشت رو میگیره   تعریف اسلاگ
        slug = self.kwargs.get('slug')
        # اینجا تعیین کردیم که از مدل .. اسلاگ برابر با اسلاگه
        article = get_object_or_404(Post, Slug=slug, status='p')

        ip_address = self.request.META['ip_address']
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)

        return article


class Article_Create(AuthorsAccessMixin, FormMixin, FieldsMixin, CreateView):
    model = Post
    template_name = 'registration/article-create-update.html'

    def get_success_url(self):
        return reverse_lazy('dashboard:home')


class Article_Update(AuthorsAccessMixin, FormMixin, FieldsMixin, UpdateView):
    model = Post
    template_name = 'registration/article-create-update.html'


class AuthorDelete(SuperUserAccessMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
    template_name = 'registration/article_confirm_delete.html'


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    form_class = UserForms
    success_url = reverse_lazy('account:profile')

    def get_object(self):

        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user

        })
        return kwargs


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('dashboard:password_change_done')


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy('dashboard:home')
        else:
            return reverse_lazy('dashboard:profile')
