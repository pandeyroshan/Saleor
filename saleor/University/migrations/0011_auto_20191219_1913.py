# Generated by Django 2.2 on 2019-12-19 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('University', '0010_representativepush_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='consignment',
            name='commissionPercentage',
            field=models.PositiveIntegerField(default=2, verbose_name='Commission Percentage'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='consignment',
            name='totalCommission',
            field=models.IntegerField(blank=True),
        ),
    ]
