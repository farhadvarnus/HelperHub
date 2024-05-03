# Generated by Django 5.0.4 on 2024-05-03 11:30

import django.db.models.deletion
import django.utils.timezone
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IpAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='آدرس آیپی')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titles', models.CharField(max_length=200, verbose_name='عنوان دسته بندی')),
                ('slugs', models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='آدرس دسته بندی')),
                ('statuses', models.BooleanField(default=True, verbose_name='آیا نمایش داده شود؟')),
                ('positions', models.IntegerField(verbose_name='پوزیشن')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='blog.category', verbose_name='زیر دسته')),
            ],
            options={
                'verbose_name': 'عنوان دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
                'ordering': ['parent__id', 'positions'],
            },
        ),
        migrations.CreateModel(
            name='ArticleHits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Created', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('ip_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.ipaddress')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان مقاله')),
                ('Slug', models.SlugField(max_length=100, unique=True, verbose_name='آدرس مقاله')),
                ('content', models.TextField(verbose_name='توضیحات')),
                ('counted_view', models.IntegerField(default=0)),
                ('image', models.ImageField(default='blog/default.jpg', upload_to='blog/', verbose_name='تصویر مقاله')),
                ('Publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان انتشار')),
                ('Created', models.DateTimeField(auto_now_add=True)),
                ('Updated', models.DateTimeField(auto_now=True)),
                ('is_spacial', models.BooleanField(default=False, verbose_name='مقاله ویژه')),
                ('status', models.CharField(choices=[('d', 'پیشنویس'), ('p', 'منتشر شده'), ('i', 'در حال بررسی'), ('b', 'برگشت داده شده')], max_length=1, verbose_name='وضعیت')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('published_date', models.DateTimeField(null=True)),
                ('like', models.IntegerField(default=0)),
                ('dislike', models.IntegerField(default=0)),
                ('Category', models.ManyToManyField(related_name='articles', to='blog.category', verbose_name='دسته بندی')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
                ('hits', models.ManyToManyField(blank=True, related_name='hits', through='blog.ArticleHits', to='blog.ipaddress', verbose_name='بازدیدها')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'مقاله',
                'verbose_name_plural': 'مقالات',
                'ordering': ['-created_date'],
            },
        ),
        migrations.AddField(
            model_name='articlehits',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post'),
        ),
    ]
