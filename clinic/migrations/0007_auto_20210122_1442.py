# Generated by Django 3.1.5 on 2021-01-22 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0006_auto_20210122_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dichvukham',
            name='tyle_tt',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
