# Generated by Django 2.2 on 2019-12-13 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('University', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='collegeLocationURL',
            field=models.URLField(default='Madhya Pradesh', max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='university',
            name='collegeLocation',
            field=models.CharField(max_length=500),
        ),
    ]
