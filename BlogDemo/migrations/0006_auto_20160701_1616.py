# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogDemo', '0005_auto_20160701_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_status',
            field=models.CharField(default='\u672a\u8bfb', max_length=10, verbose_name='\u8bc4\u8bba\u72b6\u6001', choices=[(b'R', '\u5df2\u8bfb'), (b'N', '\u672a\u8bfb')]),
        ),
    ]
