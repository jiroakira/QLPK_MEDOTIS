from clinic.models import TinhTrangPhongKham
from django.contrib import admin
from .models import (
    BaiDang, 
    ChuoiKham, 
    DichVuKham, 
    FileKetQua, 
    FileKetQuaChuyenKhoa, 
    FileKetQuaTongQuat,  
    KetQuaChuyenKhoa, 
    KetQuaTongQuat, 
    LichHenKham,
    PhanKhoaKham, 
    PhongChucNang, 
    PhongKham, 
    TrangThaiChuoiKham, 
    TrangThaiKhoaKham, 
    TrangThaiLichHen, 
    User, 
    BacSi
)

admin.site.register(User)
admin.site.register(PhongChucNang)
admin.site.register(LichHenKham)
admin.site.register(TrangThaiLichHen)
admin.site.register(PhanKhoaKham)
admin.site.register(ChuoiKham)
admin.site.register(KetQuaTongQuat)
admin.site.register(KetQuaChuyenKhoa)
admin.site.register(FileKetQua)
admin.site.register(DichVuKham)
admin.site.register(TrangThaiChuoiKham)
admin.site.register(TrangThaiKhoaKham)
admin.site.register(FileKetQuaTongQuat)
admin.site.register(FileKetQuaChuyenKhoa)
admin.site.register(BaiDang)
admin.site.register(BacSi)
admin.site.register(PhongKham)
admin.site.register(TinhTrangPhongKham)
