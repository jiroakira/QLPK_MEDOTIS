# Generated by Django 3.1.7 on 2021-04-02 02:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('medicine', '0014_thuoclog_bao_hiem'),
        ('finance', '0005_hoadonnhaphang'),
    ]

    operations = [
        migrations.CreateModel(
            name='NhapHang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_luong', models.PositiveIntegerField(blank=True, null=True)),
                ('bao_hiem', models.BooleanField(default=False)),
                ('thoi_gian_tao', models.DateTimeField(blank=True, editable=False, null=True)),
                ('thoi_gian_cap_nhat', models.DateTimeField(blank=True, null=True)),
                ('hoa_don', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.hoadonnhaphang')),
                ('thuoc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medicine.thuoc')),
            ],
            options={
                'verbose_name': 'Nhập Hàng',
            },
        ),
        migrations.CreateModel(
            name='HoaDonXuatHang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ma_hoa_don', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('thoi_gian_tao', models.DateTimeField(blank=True, editable=False, null=True)),
                ('thoi_gian_cap_nhat', models.DateTimeField(blank=True, null=True)),
                ('nguoi_phu_trach', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Hóa Đơn Nhập Hàng',
            },
        ),
    ]