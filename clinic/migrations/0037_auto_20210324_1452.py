# Generated by Django 3.1.7 on 2021-03-24 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0036_auto_20210324_1446'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('can_add_user', 'Thêm người dùng'), ('can_add_staff_user', 'Thêm nhân viên'), ('can_change_user_info', 'Chỉnh sửa người dùng'), ('can_change_staff_user_info', 'Chỉnh sửa nhân viên'), ('can_change_password_user', 'Thay đổi mật khẩu người dùng'), ('can_change_password_staff_user', 'Thay đổi mật khẩu nhân viên'), ('can_view_user_info', 'Xem người dùng'), ('can_view_staff_user_info', 'Xem nhân viên'), ('can_delete_user', 'Xóa người dùng'), ('can_delete_staff_user', 'Xóa nhân viên'), ('general_view', 'Xem Tổng Quan Trang Chủ'), ('reception_department_module_view', 'Phòng Ban Lễ Tân'), ('finance_department_module_view', 'Phòng Ban Tài Chính'), ('specialist_department_module_view', 'Phòng Ban Chuyên Gia'), ('medicine_department_module_view', 'Phòng Ban Thuốc'))},
        ),
    ]
