# Generated by Django 3.0.4 on 2020-06-05 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_auto_20200605_0807'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='source_code',
            field=models.TextField(null=True),
        ),
    ]
