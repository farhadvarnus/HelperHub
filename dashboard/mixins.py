from django.http import Http404
from django.shortcuts import redirect
from blog.models import Post


class FieldsMixin():
    def dispatch(self, request, *args,  **kwargs):
        self.fields = ['author', 'title', 'Slug', 'Category',
                       'content', 'image',
                       'Publish', 'is_spacial', 'status']
        if request.user.is_superuser:
            self.fields.append('author',)
        return super().dispatch(request, *args, **kwargs)


class FormMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.Status == 'i':
                self.obj.Status = 'd'
        return super().form_valid(form)


class AuthorAccessMixin():
    def dispatch(self, request, pk, *args,  **kwargs):
        # article = get_object_or_404(Article, pk=pk)
        if Article.author == request.user and Post.Status in ['d', 'b'] or \
                request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('شما نمیتوانید این صفحه را مشاده کنید.')


class SuperUserAccessMixin():
    def dispatch(self, request, *args,  **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('شما نمیتوانید این صفحه را مشاده کنید.')


class AuthorsAccessMixin():
    def dispatch(self, request, *args,  **kwargs):
        if request.user.is_authenticated:
            if request.user.is_author or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect('account:profile')

        else:
            return redirect('login')
