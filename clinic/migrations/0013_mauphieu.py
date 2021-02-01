# Generated by Django 3.1.5 on 2021-01-27 01:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0012_auto_20210125_0902'),
    ]

    operations = [
        migrations.CreateModel(
            name='MauPhieu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten_mau', models.CharField(blank=True, max_length=255, null=True)),
                ('noi_dung', models.TextField()),
                ('thoi_gian_tao', models.DateTimeField(blank=True, editable=False, null=True)),
                ('thoi_gian_cap_nhat', models.DateTimeField(blank=True, null=True)),
                ('dich_vu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic.dichvukham')),
            ],
        ),
    ]