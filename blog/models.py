from django.db import models
from accounts.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils.html import format_html
from django.utils import timezone
from taggit.managers import TaggableManager


# Create your models here.


# class Category(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

# class Post(models.Model):
#     image = models.ImageField(upload_to='blog/', default='blog/default.jpg')
#     tags = TaggableManager(blank=True)
#     category = models.ManyToManyField(Category)
#     author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     counted_view = models.IntegerField(default=0)
#     status = models.BooleanField(default=False)
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)
#     published_date = models.DateTimeField(null=True)
#     like = models.IntegerField(default=0)
#     dislike = models.IntegerField(default=0)

#     class Meta:
#         ordering = ["-created_date"]

#     def __str__(self):
#         return "{}- {}".format(self.title, self.id)

#     def get_absolute_url(self):
#         return reverse("singe_blog", kwargs={'pid': self.id})


####################################


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(Status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(statuses=True)


class IpAddress(models.Model):
    # _(""), protocol="both", unpack_ipv4=False ,
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آیپی')


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name='children',
                               verbose_name='زیر دسته')

    titles = models.CharField(max_length=200, verbose_name="عنوان دسته بندی")
    slugs = models.SlugField(max_length=100, unique=True,
                             verbose_name="آدرس دسته بندی",
                             blank=True, null=True)
    statuses = models.BooleanField(
        default=True, verbose_name="آیا نمایش داده شود؟")
    positions = models.IntegerField(verbose_name="پوزیشن")

    class Meta:
        verbose_name = "عنوان دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['parent__id', 'positions']

    def __str__(self):
        return self.titles

    def save(self, *args, **kwargs):
        if not self.slugs:
            self.slugs = slugify(self.titles)
        super(Category, self).save(*args, **kwargs)

    objects = CategoryManager()


class Post(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیشنویس'),
        ('p', 'منتشر شده'),
        ('i', 'در حال بررسی'),
        ('b', 'برگشت داده شده'),
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                               related_name='articles', verbose_name='نویسنده')
    title = models.CharField(max_length=200, verbose_name='عنوان مقاله')
    Slug = models.SlugField(max_length=100, unique=True,
                            verbose_name='آدرس مقاله')
    Category = models.ManyToManyField(
        Category, verbose_name="دسته بندی", related_name='articles')
    content = models.TextField(verbose_name='توضیحات')
    counted_view = models.IntegerField(default=0)

    image = models.ImageField(
        upload_to='blog/', default='blog/default.jpg',
        verbose_name='تصویر مقاله')
    tags = TaggableManager(blank=True)
    Publish = models.DateTimeField(
        default=timezone.now, verbose_name='زمان انتشار')
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    is_spacial = models.BooleanField(default=False, verbose_name="مقاله ویژه")
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    hits = models.ManyToManyField(
        IpAddress, through='ArticleHits', blank=True,
        related_name='hits',
        verbose_name='بازدیدها')

    class Meta():
        ordering = ["-created_date"]
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return "{}- {}".format(self.title, self.id)

    def get_absolute_url(self):
        return reverse("singe_blog", kwargs={'pid': self.id})

    # def jpublish(self):
    #     return jalali_converter(self.Publish)
    # jpublish.short_description = 'زمان انتشار'

    def category_to_str(self):
        return "، ".join([categori.titles for categori in
                          self.Category.active()])
    category_to_str.short_description = "دسته بندی "

    objects = ArticleManager()

    def Thumbnail_tag(self):
        return format_html(
            "<img width=120 hight=90 style='border-radius:5px' \
                src='{}' >".format(self.Thumbnail.url))
    Thumbnail_tag.short_description = 'تصویر'


class ArticleHits(models.Model):
    article = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IpAddress, on_delete=models.CASCADE)
    Created = models.DateTimeField(auto_now_add=True)

    status = models.BooleanField(default=False)
