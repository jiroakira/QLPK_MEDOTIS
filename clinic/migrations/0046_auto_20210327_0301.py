# Generated by Django 3.1.7 on 2021-03-26 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0045_auto_20210326_1447'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tinhtrangphongkham',
            options={'verbose_name': 'Tình Trạng Phòng Khám', 'verbose_name_plural': 'Tình Trạng Phòng Khám'},
        ),
        migrations.AddField(
            model_name='dichvukham',
            name='don_gia_bhyt',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='tinhtrangphongkham',
            name='ip_range_end',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='tinhtrangphongkham',
            name='ip_range_start',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
