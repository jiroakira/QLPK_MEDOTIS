# Generated by Django 3.1.5 on 2021-02-01 02:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0018_ketquachuyenkhoa_phan_khoa_kham'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phankhoakham',
            name='benh_nhan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='phankhoakham',
            name='dich_vu_kham',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='phan_khoa_dich_vu', to='clinic.dichvukham'),
        ),
    ]