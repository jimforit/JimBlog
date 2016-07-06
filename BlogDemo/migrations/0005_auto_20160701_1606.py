# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogDemo', '0004_auto_20160701_1246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment_type',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_status',
            field=models.CharField(default='\u672a\u8bfb', max_length=10, verbose_name='\u8bc4\u8bba\u7c7b\u578b', choices=[(b'R', '\u5df2\u8bfb'), (b'N', '\u672a\u8bfb')]),
        ),
    ]
