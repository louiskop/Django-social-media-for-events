# Generated by Django 2.0.5 on 2018-09-18 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0007_auto_20180917_1856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='model_pic',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='imgs/None/no-img.jpg', upload_to='imgs/'),
        ),
    ]