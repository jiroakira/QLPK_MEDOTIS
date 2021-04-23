# Generated by Django 3.2 on 2021-04-23 10:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clinic', '0048_auto_20210423_1746'),
        ('medicine', '0011_auto_20210326_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='NhomThuoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ma_nhom', models.CharField(blank=True, max_length=255, null=True)),
                ('ten_nhom', models.CharField(blank=True, max_length=255, null=True)),
                ('thoi_gian_tao', models.DateTimeField(auto_now_add=True, null=True)),
                ('thoi_gian_cap_nhat', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Nhóm Thuốc',
                'verbose_name_plural': 'Nhóm Thuốc',
            },
        ),
        migrations.AddField(
            model_name='donthuoc',
            name='benh_nhan_vang_lai',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='thuoc',
            name='gia_bhyt',
            field=models.IntegerField(max_length=50, null=True, verbose_name='Giá bảo hiểm y tế'),
        ),
        migrations.AddField(
            model_name='thuoc',
            name='stt',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='thuoclog',
            name='bao_hiem',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='donthuoc',
            name='bac_si_ke_don',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bac_si_ke_don', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='donthuoc',
            name='benh_nhan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='don_thuoc', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='donthuoc',
            name='chuoi_kham',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='don_thuoc_chuoi_kham', to='clinic.chuoikham'),
        ),
        migrations.AlterField(
            model_name='donthuoc',
            name='trang_thai',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='medicine.trangthaidonthuoc'),
        ),
        migrations.AlterField(
            model_name='kedonthuoc',
            name='thuoc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medicine.thuoc'),
        ),
        migrations.AlterField(
            model_name='thuoc',
            name='don_gia',
            field=models.IntegerField(max_length=255, null=True, verbose_name='Đơn giá'),
        ),
        migrations.AlterField(
            model_name='thuoc',
            name='don_gia_tt',
            field=models.IntegerField(max_length=255, null=True, verbose_name='Đơn giá thành tiền'),
        ),
        migrations.AlterField(
            model_name='thuoc',
            name='ham_luong',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Hàm lượng'),
        ),
        migrations.AlterField(
            model_name='thuoc',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='thuoc',
            name='loai_thuoc',
            field=models.CharField(blank=True, choices=[('1', 'Tân Dược'), ('2', 'Chế phẩm YHCT'), ('3', 'Vị thuốc YHCT'), ('4', 'Phóng xạ'), ('5', 'Thực phẩm bảo vệ sức khỏe'), ('6', 'Vật Tư Y Tế')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='thuoc',
            name='ma_thuoc',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='thuoc',
            name='ngay_gio_tao',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Ngày giờ tạo'),
        ),
        migrations.AlterField(
            model_name='thuoc',
            name='nuoc_sx',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='thuoc',
            name='quyet_dinh',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='thuoc',
            name='thoi_gian_cap_nhat',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='thuoc',
            name='nhom_thuoc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nhom_thuoc', to='medicine.nhomthuoc'),
        ),
    ]