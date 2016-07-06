# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogDemo', '0003_auto_20160630_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_reminder',
            field=models.ForeignKey(related_name='comment_reminder', verbose_name='\u63d0\u9192\u4eba', to='BlogDemo.User', null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_type',
            field=models.CharField(default='\u8bc4\u8bba', max_length=10, verbose_name='\u8bc4\u8bba\u7c7b\u578b', choices=[(b'R', '\u56de\u590d'), (b'C', '\u8bc4\u8bba')]),
        ),
    ]
