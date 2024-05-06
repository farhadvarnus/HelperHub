from django import forms
from blog.models import Post
from captcha.fields import CaptchaField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class PostForm(forms.ModelForm):
    captcha = CaptchaField()
    content = forms.CharField(widget=SummernoteWidget())

    class Meta:

        model = Post
        fields = "__all__"
