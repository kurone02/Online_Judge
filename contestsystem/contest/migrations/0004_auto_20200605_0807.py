# Generated by Django 3.0.4 on 2020-06-05 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_submission'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='langUsed',
            new_name='language',
        ),
        migrations.RenameField(
            model_name='submission',
            old_name='memUsed',
            new_name='memory',
        ),
    ]
