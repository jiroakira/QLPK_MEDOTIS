# Generated by Django 3.1.5 on 2021-01-20 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0004_auto_20210120_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='can_nang',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
