# Generated by Django 2.0.5 on 2018-09-17 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0006_auto_20180917_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='model_pic',
            field=models.ImageField(default='imgs/None/no-img.jpg', height_field='200px', upload_to='imgs/', width_field='200px'),
        ),
    ]
