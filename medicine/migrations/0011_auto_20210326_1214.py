# Generated by Django 3.1.7 on 2021-03-26 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0010_auto_20210326_1025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='congty',
            options={'permissions': (('can_add_company', 'Thêm nguồn cung'), ('can_change_company', 'Thay đổi nguồn cung'), ('can_view_company', 'Xem nguồn cung'), ('can_delete_company', 'Xóa nguồn cung'), ('can_export_list_of_company', 'Xuất danh sách nguồn cung')), 'verbose_name': 'Công Ty', 'verbose_name_plural': 'Công Ty'},
        ),
        migrations.AlterModelOptions(
            name='vattu',
            options={'permissions': (('can_add_medical_supplies', 'Thêm vật tư y tế'), ('can_change_medical_supplies', 'Thay đổi vật tư y tế'), ('can_view_medical_supplies', 'Xem vật tư y tế'), ('can_delete_medical_supplies', 'Xóa vật tư y tế'), ('can_export_medical_supplies_list', 'Xuất danh sách vật tư y tế'), ('can_listed_supplies_at_the_end_of_month', 'Thống kê vật tư cuối tháng'), ('can_add_supplies_using_excel_file', 'Thêm vật tư bằng Excel File')), 'verbose_name': 'Vật Tư', 'verbose_name_plural': 'Vật Tư'},
        ),
    ]
