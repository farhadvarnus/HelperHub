from django.shortcuts import render
from .forms import ContactForm
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
# Create your views here.


def index_view(request):
    posts = Post.objects.all().order_by('-like')[:5]
    form = ContactForm()
    users = User.objects.all().count()
    post_count = Post.objects.all().count()
    context = {'posts': posts, 'form': form,
               'users': users, 'post_count': post_count}
    return render(request, 'mysite/index.html', context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # form.instance.name = "unknown"
            form.save()
            messages.add_message(request, messages.SUCCESS, 'SUCCESS!!!')

        else:
            messages.add_message(request, messages.ERROR, 'FAILD!!!')

    form = ContactForm()
    return render(request, "mysite/index.html", {"form": form})
