# Generated by Django 3.1.7 on 2021-03-26 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0042_auto_20210326_1144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dichvukham',
            options={'permissions': (('can_add_service', 'Thêm dịch vụ kỹ thuật'), ('can_add_service_with_excel_file', 'Thêm dịch vụ kỹ thuật bằng Excel File'), ('can_change_service', 'Thay đổi dịch vụ kỹ thuật'), ('can_view_service', 'Xem dịch vụ kỹ thuật'), ('can_delete_service', 'Xóa dịch vụ kỹ thuật'), ('can_view_service_price', 'Xem giá dịch vụ kỹ thuật'), ('can_export_list_of_service', 'Xuất danh sách dịch vụ kỹ thuật')), 'verbose_name': 'Dịch Vụ Khám', 'verbose_name_plural': 'Dịch Vụ Khám'},
        ),
    ]
