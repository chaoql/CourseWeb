# Generated by Django 3.2.19 on 2023-07-03 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_notice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.CharField(default='', max_length=1000, verbose_name='访问地址'),
        ),
    ]