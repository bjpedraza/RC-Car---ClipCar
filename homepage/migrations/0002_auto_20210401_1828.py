# Generated by Django 3.1.6 on 2021-04-01 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='video',
            field=models.FileField(upload_to='videos/%y'),
        ),
    ]
