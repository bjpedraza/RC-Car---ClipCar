# Generated by Django 3.1.6 on 2021-04-01 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0005_auto_20210401_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]