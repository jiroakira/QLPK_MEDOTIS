# Generated by Django 3.2 on 2021-04-25 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0017_thuoc_stt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thuoc',
            name='nhom_thuoc',
        ),
        migrations.AddField(
            model_name='thuoc',
            name='nhom_thuoc',
            field=models.ManyToManyField(related_name='nhom_thuoc', to='medicine.NhomThuoc'),
        ),
    ]
