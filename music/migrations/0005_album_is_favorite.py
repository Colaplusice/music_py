# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("music", "0004_auto_20180228_1329")]

    operations = [
        migrations.AddField(
            model_name="album",
            name="is_favorite",
            field=models.BooleanField(default=False),
        )
    ]
