# Generated by Django 3.1.6 on 2021-02-21 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0025_phuongxa_quanhuyen_tinhthanh'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('district_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ward', to='clinic.district')),
            ],
        ),
        migrations.RemoveField(
            model_name='quanhuyen',
            name='tinh_id',
        ),
        migrations.DeleteModel(
            name='PhuongXa',
        ),
        migrations.DeleteModel(
            name='QuanHuyen',
        ),
        migrations.DeleteModel(
            name='TinhThanh',
        ),
        migrations.AddField(
            model_name='district',
            name='province_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='district', to='clinic.province'),
        ),
    ]