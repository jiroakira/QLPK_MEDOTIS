# Generated by Django 3.1.5 on 2021-01-23 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0003_auto_20210122_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thuoc',
            name='duong_dung',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Đường dùng'),
        ),
    ]
