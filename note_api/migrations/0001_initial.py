# Generated by Django 4.0.4 on 2022-06-05 09:14

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_important', models.BooleanField(default=False, verbose_name='Важно')),
                ('state', models.PositiveSmallIntegerField(choices=[(0, 'Активнo'), (1, 'Отложенo'), (2, 'Выполненo')], default=0)),
                ('inner', models.TextField(verbose_name='Текст заметки')),
                ('is_public', models.BooleanField(default=False, verbose_name='Публичная')),
                ('publication_date', models.DateTimeField(default=datetime.datetime(2022, 6, 6, 12, 14, 31, 781284), verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Заметка',
                'verbose_name_plural': 'Заметки',
            },
        ),
    ]
