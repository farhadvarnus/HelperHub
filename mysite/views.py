from django.shortcuts import render
from .forms import ContactForm
from django.contrib import messages
# Create your views here.


def index_view(request):
    return render(request, 'mysite/index.html')


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
