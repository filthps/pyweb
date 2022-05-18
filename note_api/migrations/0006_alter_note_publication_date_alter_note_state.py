# Generated by Django 4.0.4 on 2022-05-14 18:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note_api', '0005_alter_note_id_alter_note_publication_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 15, 21, 31, 5, 397605)),
        ),
        migrations.AlterField(
            model_name='note',
            name='state',
            field=models.PositiveSmallIntegerField(choices=[('Активнo', 0), ('Отложенo', 1), ('Выполненo', 2)], default=0, max_length=30),
        ),
    ]