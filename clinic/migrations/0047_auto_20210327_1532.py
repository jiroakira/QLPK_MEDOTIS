# Generated by Django 3.1.7 on 2021-03-27 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0046_auto_20210327_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
