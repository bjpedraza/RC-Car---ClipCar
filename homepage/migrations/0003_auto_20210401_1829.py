# Generated by Django 3.1.6 on 2021-04-01 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20210401_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='title',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='videos',
            name='video',
            field=models.FileField(upload_to='videos/'),
        ),
    ]
