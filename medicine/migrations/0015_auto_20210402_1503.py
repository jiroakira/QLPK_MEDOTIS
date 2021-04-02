# Generated by Django 3.1.7 on 2021-04-02 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0014_thuoclog_bao_hiem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thuoc',
            name='loai_thuoc',
            field=models.CharField(blank=True, choices=[('1', 'Tân Dược'), ('2', 'Chế phẩm YHCT'), ('3', 'Vị thuốc YHCT'), ('4', 'Phóng xạ'), ('5', 'Thực phẩm bảo vệ sức khỏe'), ('6', 'Vật Tư Y Tế')], max_length=255, null=True),
        ),
    ]
