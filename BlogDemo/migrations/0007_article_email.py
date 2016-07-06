# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogDemo', '0006_auto_20160701_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='email',
            field=models.EmailField(default=b'jimforit@163.com', max_length=256, verbose_name='\u90ae\u7bb1\u5730\u5740'),
        ),
    ]
