from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from blog.models import Post
from .models import User
from .forms import UserForms, SignupForm
from .mixins import (
    FieldsMixin,
    FormMixin,
    SuperUserAccessMixin,
    AuthorsAccessMixin, )
from django.urls import reverse_lazy
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str as force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import EmailMessage


class Article_list(AuthorsAccessMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()
        else:
            return Post.objects.filter(author=self.request.user)


class Article_Create(AuthorsAccessMixin, FormMixin, FieldsMixin, CreateView):
    model = Post
    template_name = 'registration/article-create-update.html'


class Article_Update(AuthorsAccessMixin, FormMixin, FieldsMixin, UpdateView):
    model = Post
    template_name = 'registration/article-create-update.html'


class AuthorDelete(SuperUserAccessMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('accounts:index')
    template_name = 'registration/article_confirm_delete.html'


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    form_class = UserForms
    success_url = reverse_lazy('dashboard:profile')

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


class PasswordChangeDoneView(PasswordChangeView):
    success_url = reverse_lazy('dashboard:profile')


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy('accounts:index')
        else:
            return reverse_lazy('accounts:profile')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/authenticated.html')
    else:
        return redirect(reverse('failed'))


def authenticated_page(request):
    return render(request, 'registration/authenticated.html')


def confirmation_page(request):
    return render(request, 'registration/confirmation.html')


def failed_page(request):
    return render(request, 'registration/failed.html')


# def authenticated_page(request):
    # return render(request, 'registration/authenticated.html')


class SignUp(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False

        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعالسازی اکانت'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return redirect('confirmation/')


def email_invalid(request):
    return render(request, 'registration/email_invalid.html')
