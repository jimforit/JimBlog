# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=70, verbose_name='\u6807\u9898')),
                ('body', models.TextField(verbose_name='\u6b63\u6587')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65f6\u95f4')),
                ('status', models.CharField(max_length=1, verbose_name='\u6587\u7ae0\u72b6\u6001', choices=[(b'd', b'draft'), (b'p', b'Published')])),
                ('abstract', models.CharField(help_text='\u53ef\u9009\uff0c\u5982\u82e5\u4e3a\u7a7a\u5c06\u6458\u53d6\u6b63\u6587\u7684\u524d54\u4e2a\u5b57\u7b26', max_length=54, null=True, verbose_name='\u6587\u7ae0\u6458\u8981', blank=True)),
                ('views', models.PositiveIntegerField(default=0, verbose_name='\u6d4f\u89c8\u91cf')),
                ('likes', models.PositiveIntegerField(default=0, verbose_name='\u70b9\u8d5e\u6570')),
                ('topped', models.BooleanField(default=False, verbose_name='\u7f6e\u9876')),
            ],
            options={
                'ordering': ['-last_modified_time'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='\u7c7b\u540d')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65f6\u95f4')),
            ],
            options={
                'ordering': ['-last_modified_time'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_content', models.TextField(verbose_name='\u8bc4\u8bba\u5185\u5bb9')),
                ('comment_time', models.DateTimeField(auto_now=True, verbose_name='\u8bc4\u8bba\u65f6\u95f4')),
                ('article', models.ForeignKey(verbose_name='\u5f52\u5c5e\u6587\u7ae0', to='BlogDemo.Article')),
            ],
            options={
                'ordering': ['comment_time'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='\u7528\u6237\u540d')),
                ('passwd', models.CharField(max_length=20, null=True, verbose_name='\u5bc6\u7801')),
                ('status', models.CharField(default=b'online', max_length=10, verbose_name='\u72b6\u6001', choices=[(b'invisible', '\u9690\u8eab'), (b'online', '\u5728\u7ebf'), (b'offline', '\u79bb\u7ebf')])),
                ('last_login_time', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4e00\u6b21\u767b\u5f55\u65f6\u95f4')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_user',
            field=models.ForeignKey(related_name='comment_user', verbose_name='\u8bc4\u8bba\u4eba', to='BlogDemo.User'),
        ),
        migrations.AddField(
            model_name='article',
            name='auther',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u4f5c\u8005', to='BlogDemo.User', null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u5206\u7c7b', to='BlogDemo.Category', null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='likes_user',
            field=models.ManyToManyField(related_name='user_hit_likes', null=True, verbose_name='\u70b9\u8d5e\u4eba', to='BlogDemo.User'),
        ),
    ]
