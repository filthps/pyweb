# Generated by Django 4.0.4 on 2022-06-03 15:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_initial'),
        ('note_api', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='comments',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='comments.comment'),
        ),
        migrations.AlterField(
            model_name='note',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 4, 18, 49, 32, 808280), verbose_name='Дата публикации'),
        ),
    ]