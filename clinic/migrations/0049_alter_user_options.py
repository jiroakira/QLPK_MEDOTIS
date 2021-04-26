# Generated by Django 3.2 on 2021-04-26 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0048_auto_20210423_1746'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('can_add_user', 'Thêm người dùng'), ('can_add_staff_user', 'Thêm nhân viên'), ('can_change_user_info', 'Chỉnh sửa người dùng'), ('can_change_staff_user_info', 'Chỉnh sửa nhân viên'), ('can_change_password_user', 'Thay đổi mật khẩu người dùng'), ('can_change_password_staff_user', 'Thay đổi mật khẩu nhân viên'), ('can_view_user_info', 'Xem người dùng'), ('can_view_staff_user_info', 'Xem nhân viên'), ('can_delete_user', 'Xóa người dùng'), ('can_delete_staff_user', 'Xóa nhân viên'), ('general_view', 'Xem Tổng Quan Trang Chủ'), ('reception_department_module_view', 'Phòng Ban Lễ Tân'), ('finance_department_module_view', 'Phòng Ban Tài Chính'), ('specialist_department_module_view', 'Phòng Ban Chuyên Gia'), ('preclinical_department_module_view', 'Phòng Ban Lâm Sàng'), ('medicine_department_module_view', 'Phòng Ban Thuốc'), ('general_revenue_view', 'Xem Doanh Thu Phòng Khám'), ('can_view_checkout_list', 'Xem Danh Sách Thanh Toán Tài Chính'), ('export_insurance_data', 'Xuất Bảo Hiểm Tài Chính'), ('can_export_list_of_patient_insurance_coverage', 'Xuất Danh Sách Bệnh Nhân Bảo Hiểm Chi Trả'), ('can_view_list_of_patient', 'Xem Danh Sách Bệnh Nhân Chờ'), ('can_bao_cao_thuoc', 'Báo Cáo Thuốc'), ('can_export_list_import_export_general_medicines', 'Xuất Danh Sách Xuất Nhập Tồn Tổng Hợp Thuốc'), ('can_export_soon_expired_list_medicines', 'Xuất Danh Sách Thuốc Sắp Hết Hạn'))},
        ),
    ]
