from finance.models import HoaDonChuoiKham, HoaDonThuoc, HoaDonLamSang
from medicine.serializers import CongTySerializer, ThuocSerializer, ThuocSerializerSimple
# from finance.serializers import HoaDonChuoiKhamSerializer, HoaDonThuocSerializer
from os import set_inheritable
from django.http.request import validate_host
from rest_framework import fields, serializers
from django.contrib.auth import get_user_model
from .models import (
    BaiDang, ChiSoXetNghiem, ChiTietChiSoXetNghiem, 
    DichVuKham, District, 
    FileKetQua, 
    FileKetQuaChuyenKhoa, 
    FileKetQuaTongQuat, HtmlKetQua, 
    KetQuaChuyenKhoa, 
    KetQuaTongQuat, KetQuaXetNghiem, 
    LichHenKham, MauPhieu, 
    PhanKhoaKham, 
    PhongChucNang, 
    PhongKham, 
    ProfilePhongChucNang, 
    TrangThaiChuoiKham, 
    TrangThaiKhoaKham, 
    TrangThaiLichHen, 
    ChuoiKham, 
    BacSi,
    TinhTrangPhongKham, Ward, send_func_room_info,
)
from medicine.models import DonThuoc, KeDonThuoc, NhomVatTu, VatTu

User = get_user_model()

class ChildUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('id', 'so_dien_thoai', 'ho_ten', 'email', 'cmnd_cccd', 'chuc_nang') 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('id', 'so_dien_thoai', 'ho_ten', 'email', 'cmnd_cccd', 'dia_chi', 'ngay_sinh', 'gioi_tinh', 'ma_benh_nhan', 'dan_toc', 'anh_dai_dien', 'ma_so_bao_hiem')
        extra_kwargs = {'password': {'write_only': True}}

    # TODO create and update child instance of user
    # TODO review again

class UserLoginSerializer(serializers.Serializer):
    so_dien_thoai = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class DangKiSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('so_dien_thoai', 'password', 'ho_ten', 'cmnd_cccd', 'dia_chi')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            ho_ten = validated_data['ho_ten'], 
            so_dien_thoai = validated_data['so_dien_thoai'], 
            password = validated_data['password'],
            cmnd_cccd = validated_data['cmnd_cccd'], 
            dia_chi = validated_data['dia_chi']
        )
        return user

class DichVuKhamSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = DichVuKham
        fields = ('id', 'ma_dvkt', 'ten_dvkt', 'ma_gia', 'quyet_dinh', 'cong_bo', 'ma_cosokcb')

class TrangThaiLichHenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrangThaiLichHen
        fields = '__all__'

    # def create(self, validated_data):
    #     ten_dich_vu = validated_data.get('ten_dich_vu')
    #     dich_vu = DichVuKham.objects.get_or_create(ten_dich_vu = ten_dich_vu)[0]
    #     return dich_vu

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['bac_si_phu_trach'] = UserSerializer(instance.bac_si_phu_trach).data
    #     return response

class PhongChucNangSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhongChucNang
        fields = '__all__'

    def create(self, validated_data):
        ten_phong_chuc_nang = validated_data.get('ten_phong_chuc_nang')
        phong_chuc_nang = PhongChucNang.objects.get_or_create(ten_phong_chuc_nang = ten_phong_chuc_nang)[0]
        return phong_chuc_nang

    def to_representation(self, instance):

        response = super().to_representation(instance)
        response['dich_vu_kham'] = DichVuKhamSerializer(instance.dich_vu_kham).data
        return response

class ProfilePhongChucNangSerializer(serializers.ModelSerializer):
    phong_chuc_nang = PhongChucNangSerializer()
    class Meta:
        model = ProfilePhongChucNang
        fields = '__all__'

class TrangThaiLichHenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrangThaiLichHen
        fields = '__all__'


class LichHenKhamSerializer(serializers.ModelSerializer):
    benh_nhan = UserSerializer()
    nguoi_phu_trach = UserSerializer()
    trang_thai = TrangThaiLichHenSerializer()
    class Meta:
        model = LichHenKham
        fields = '__all__'

    def create(self, validated_data):
        benh_nhan = validated_data.get('benh_nhan')
        ngay_hen = validated_data.get('ngay_hen')
        thoi_gian_bat_dau = validated_data.get('thoi_gian_bat_dau')
        lich_hen = LichHenKham.objects.get_or_create(
            benh_nhan=benh_nhan,
            ngay_hen=ngay_hen,
            thoi_gian_bat_dau=thoi_gian_bat_dau
        )
        return lich_hen
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['actions'] = ''
        return response

class TrangThaiLichHenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrangThaiLichHen
        fields = '__all__'

class TrangThaiKhoaKhamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrangThaiKhoaKham
        fields = '__all__'

class TrangThaiChuoiKhamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrangThaiChuoiKham
        fields = '__all__'


class ChuoiKhamSerializerSimple(serializers.ModelSerializer):
    benh_nhan = UserSerializer()
    bac_si_dam_nhan = UserSerializer()
    trang_thai = TrangThaiChuoiKhamSerializer()
    class Meta:
        model = ChuoiKham
        fields = ('id', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'benh_nhan', 'bac_si_dam_nhan', 'trang_thai')

class ChuoiKhamPhanKhoaSerializer(serializers.ModelSerializer):
    trang_thai = TrangThaiChuoiKhamSerializer()
    class Meta:
        model = ChuoiKham
        fields = ('id', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'benh_nhan', 'bac_si_dam_nhan', 'trang_thai')

class FileKetQuaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileKetQua
        fields = ('id', 'file', 'thoi_gian_tao')

class FileKetQuaChuyenKhoaSerializer(serializers.ModelSerializer):
    file_ket_qua = FileKetQuaSerializer(source='file')
    class Meta:
        model = FileKetQuaChuyenKhoa
        fields = ('id', 'file_ket_qua')

class FileKetQuaTongQuatSerializer(serializers.ModelSerializer):
    file_ket_qua = FileKetQuaSerializer(source='file')
    class Meta:
        model = FileKetQuaTongQuat
        fields = ('id', 'file_ket_qua')

class KetQuaChuyenKhoaSerializer(serializers.ModelSerializer):
    file_chuyen_khoa = FileKetQuaChuyenKhoaSerializer(many=True, source='file_ket_qua_chuyen_khoa')
    class Meta:
        model = KetQuaChuyenKhoa
        fields = ('id', 'ma_ket_qua', 'mo_ta', 'ket_luan', 'file_chuyen_khoa')

class KetQuaTongQuatSerializer(serializers.ModelSerializer):
    file_tong_quat = FileKetQuaTongQuatSerializer(source='file_ket_qua_tong_quat', many=True)
    kq_chuyen_khoa = KetQuaChuyenKhoaSerializer(source='ket_qua_chuyen_khoa', many=True)
    class Meta:
        model = KetQuaTongQuat
        fields = ('id', 'ma_ket_qua', 'mo_ta', 'ket_luan', 'file_tong_quat', 'kq_chuyen_khoa')


        
class DonThuocSerializer(serializers.ModelSerializer):
    bac_si_ke_don = UserSerializer()
    benh_nhan = UserSerializer()
    class Meta:
        model = DonThuoc
        fields = '__all__'
        
class HoaDonThuocSerializer(serializers.ModelSerializer):
    don_thuoc = DonThuocSerializer()
    tong_tien = serializers.CharField(source='get_don_gia')
    class Meta:
        model = HoaDonThuoc
        fields = '__all__'
        

class HoaDonThuocSerializerSimple(serializers.ModelSerializer):
    benh_nhan = UserSerializer()
    bac_si_ke_don = UserSerializer()
    # don_thuoc = DonThuocSerializer()
    class Meta:
        model = DonThuoc
        # fields = (
        #     'id',
        #     'benh_nhan', 
        #     'bac_si_ke_don',
        #     'don_thuoc',
        #     'thoi_gian_tao',
        # )
        fields = '__all__'


class PhanKhoaKhamDichVuSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhanKhoaKham
        fields = ('id', 'chuoi_kham', 'benh_nhan', 'bac_si_lam_sang', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'dich_vu_kham')

# class PhongChucNangSerializer(serializers.ModelSerializer):
#     dich_vu_kham = DichVuKhamSerializer()
#     danh_sach_benh_nhan = PhanKhoaKhamDichVuSerializer(source='danh_sach_benh_nhan_theo_dich_vu_kham', many=
#     True)
#     class Meta:
#         model = PhongChucNang
#         fields = ('id', 'dich_vu_kham', 'ten_phong_chuc_nang', 'danh_sach_benh_nhan')

class PhongChucNangSerializerSimple(serializers.ModelSerializer):
    bac_si_phu_trach = UserSerializer()
    class Meta:
        model = PhongChucNang
        fields = "__all__"



class KetQuaChuyenKhoaSerializer(serializers.ModelSerializer):
    file_chuyen_khoa = FileKetQuaChuyenKhoaSerializer(many=True, source='file_ket_qua_chuyen_khoa')
    ten_dich_vu = serializers.CharField(source="get_ten_dich_vu")
    class Meta:
        model = KetQuaChuyenKhoa
        fields = (
            'id',
            'ten_dich_vu',
            'ma_ket_qua', 
            'mo_ta', 
            'ket_luan', 
            'file_chuyen_khoa',
            'chi_so',
            'html'

        )

class FileKetQuaTongQuatSerializer(serializers.ModelSerializer):
    file_ket_qua = FileKetQuaSerializer(source='file')
    class Meta:
        model = FileKetQuaTongQuat
        fields = ('id', 'file_ket_qua')

class KetQuaTongQuatSerializer(serializers.ModelSerializer):
    file_tong_quat = FileKetQuaTongQuatSerializer(source='file_ket_qua_tong_quat', many=True)
    kq_chuyen_khoa = KetQuaChuyenKhoaSerializer(source='ket_qua_chuyen_khoa', many=True)
    class Meta:
        model = KetQuaTongQuat
        fields = ('id', 'ma_ket_qua', 'mo_ta', 'ket_luan', 'file_tong_quat', 'kq_chuyen_khoa')

class DonThuocSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonThuoc
        fields = '__all__'

class DichVuKhamPhanKhoaSerializer(serializers.ModelSerializer):
    phong_chuc_nang = PhongChucNangSerializerSimple()
    class Meta:
        model = DichVuKham
        fields = ('id', 'ma_dvkt', 'ten_dvkt', 'ma_cosokcb', 'phong_chuc_nang')


class UserSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'ho_ten', 'so_dien_thoai')


class ChuoiKhamUserSerializer(serializers.ModelSerializer):
    bac_si_dam_nhan = UserSerializerSimple()
    class Meta:
        model = ChuoiKham
        fields = ('id', 'bac_si_dam_nhan', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc')

class LichHenKhamUserSerializer(serializers.ModelSerializer):
    trang_thai = TrangThaiLichHenSerializer()
    chuoi_kham = ChuoiKhamUserSerializer(source='danh_sach_chuoi_kham', many=True)
    class Meta:
        model = LichHenKham
        fields = ('id', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'trang_thai', 'chuoi_kham')


class LichHenKhamSerializerSimple(serializers.ModelSerializer):
    trang_thai = TrangThaiLichHenSerializer()
    class Meta:
        model = LichHenKham
        fields = ('id', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'trang_thai')

class BookLichHenKhamSerializer(serializers.Serializer):
    benh_nhan = serializers.CharField()
    thoi_gian_bat_dau = serializers.CharField()
    # class Meta:
    #     model = LichHenKham
    #     fields = ('benh_nhan', 'thoi_gian_bat_dau')

class DanhSachDonThuocSerializer(serializers.ModelSerializer):
    bac_si_ke_don = UserSerializerSimple()
    class Meta:
        model = DonThuoc
        fields = ('id', 'ma_don_thuoc', 'bac_si_ke_don')

class DonThuocSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonThuoc
        fields = '__all__'


class DanhSachPhanKhoaSerializer(serializers.ModelSerializer):
    dich_vu_kham = DichVuKhamPhanKhoaSerializer()
    trang_thai = TrangThaiKhoaKhamSerializer()
    class Meta:
        model = PhanKhoaKham
        fields = ('id', 'priority', 'dich_vu_kham', 'trang_thai')

class UserSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'ho_ten', 'so_dien_thoai')


class ChuoiKhamUserSerializer(serializers.ModelSerializer):
    bac_si_dam_nhan = UserSerializerSimple()
    class Meta:
        model = ChuoiKham
        fields = ('id', 'bac_si_dam_nhan', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc')

class LichHenKhamUserSerializer(serializers.ModelSerializer):
    trang_thai = TrangThaiLichHenSerializer()
    chuoi_kham = ChuoiKhamUserSerializer(source='danh_sach_chuoi_kham', many=True)
    class Meta:
        model = LichHenKham
        fields = ('id', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'trang_thai', 'chuoi_kham')


class LichHenKhamSerializerSimple(serializers.ModelSerializer):
    trang_thai = TrangThaiLichHenSerializer()
    class Meta:
        model = LichHenKham
        fields = ('id', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'trang_thai', 'dia_diem', 'ly_do', 'loai_dich_vu')

class BookLichHenKhamSerializer(serializers.Serializer):

    benh_nhan = serializers.CharField()
    thoi_gian_bat_dau = serializers.CharField()
    loai_dich_vu = serializers.CharField()
    ly_do = serializers.CharField()
    dia_diem = serializers.CharField()

    # class Meta:
    #     model = LichHenKham
    #     fields = ('benh_nhan', 'thoi_gian_bat_dau')

class DanhSachDonThuocSerializer(serializers.ModelSerializer):
    bac_si_ke_don = UserSerializerSimple()
    class Meta:
        model = DonThuoc
        fields = ('id', 'ma_don_thuoc', 'bac_si_ke_don')

class BaiDangSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaiDang
        fields = "__all__"
        
class NhomVatTuSerializer(serializers.ModelSerializer):
    class Meta:
        model = NhomVatTu
        fields = "__all__"

class VatTuSerializer(serializers.ModelSerializer):
    nhom_vat_tu = NhomVatTuSerializer()
    nha_thau = CongTySerializer()
    class Meta:
        model = VatTu
        fields = '__all__'
        
        
# -------- MINH Update ---------

class UserUpdateInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'ho_ten', 'so_dien_thoai', 'email', 'cmnd_cccd', 'ngay_sinh', 'gioi_tinh', 'dia_chi', 'dan_toc', 'ma_so_bao_hiem')

class UserUpdateInfoRequestSerializer(serializers.Serializer):
    benh_nhan = serializers.CharField(required=True)
    ho_ten = serializers.CharField()
    so_dien_thoai = serializers.CharField(required=True)
    email = serializers.CharField()
    cmnd_cccd = serializers.CharField()
    ngay_sinh = serializers.CharField()
    gioi_tinh = serializers.CharField()
    dia_chi = serializers.CharField()
    dan_toc = serializers.CharField()
    ma_so_bao_hiem = serializers.CharField()

class UploadAvatarSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()
    class Meta:
        fields = ['file_uploaded']

class AppointmentUpdateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LichHenKham
        fields = ('loai_dich_vu', 'dia_diem', 'ly_do', 'thoi_gian_bat_dau',)

class UpdateLichHenKhamSerializer(serializers.Serializer):
    appointment_id = serializers.CharField()
    thoi_gian_bat_dau = serializers.CharField()
    loai_dich_vu = serializers.CharField()
    ly_do = serializers.CharField()
    dia_diem = serializers.CharField()

class DichVuKhamHoaDonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DichVuKham
        fields = ('ma_dvkt', 'ten_dvkt', 'don_gia')

class HoaDonChuoiKhamThanhToanSerializer(serializers.ModelSerializer):
    dich_vu_kham = DichVuKhamHoaDonSerializer()
    class Meta:
        model = PhanKhoaKham
        fields = ('dich_vu_kham', 'bao_hiem', 'priority',)
        
class DanhSachDichVuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DichVuKham
        fields = ('ma_dvkt', 'ten_dvkt', 'don_gia')

class HoaDonLamSangSerializer(serializers.ModelSerializer):
    lich_hen = LichHenKhamSerializer()
    tong_tien = serializers.CharField(source='get_don_gia')
    class Meta:
        model = HoaDonLamSang
        fields = ('id', 'tong_tien', 'thoi_gian_tao', 'lich_hen')


# * -------------------- End -----------------------


# UPDATE BY LONG
class BacSiSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = '__all__'


class DanhSachBacSiSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta: 
        model = BacSi
        fields = '__all__'
# END


class DichVuKhamSerializer(serializers.ModelSerializer):
    phong_chuc_nang = PhongChucNangSerializerSimple()
    class Meta:
        model = DichVuKham
        fields = '__all__'

class PhanKhoaKhamSerializer(serializers.ModelSerializer):
    chuoi_kham = ChuoiKhamPhanKhoaSerializer()
    benh_nhan = UserSerializer()
    bac_si_lam_sang = UserSerializer()
    dich_vu_kham = DichVuKhamSerializer()
    class Meta:
        model = PhanKhoaKham
        fields = ('id','chuoi_kham', 'benh_nhan', 'bac_si_lam_sang', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'dich_vu_kham')

class ChuoiKhamSerializer(serializers.ModelSerializer):
    phan_khoa_kham = PhanKhoaKhamSerializer(many=True)
    benh_nhan = UserSerializer()
    bac_si_dam_nhan = UserSerializer()
    class Meta:
        model = ChuoiKham
        fields = '__all__'
 
    def create(self, validated_data):
        pass
 
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['actions'] = ''
        return response

class HoaDonChuoiKhamSerializer(serializers.ModelSerializer):
    chuoi_kham = ChuoiKhamSerializer()
    class Meta:
        model = HoaDonChuoiKham
        fields = '__all__'

class HoaDonChuoiKhamSerializerSimple(serializers.ModelSerializer):
    benh_nhan = UserSerializer()
    bac_si_dam_nhan = UserSerializer()  
    hoa_don = HoaDonChuoiKhamSerializer(read_only=True, source = 'hoa_don_dich_vu')
    class Meta:
        model = ChuoiKham
        depth = 1
        fields = (
            'id', 
            'benh_nhan', 
            'bac_si_dam_nhan',
            'trang_thai',
            'hoa_don',
            'thoi_gian_tao',
        )

class DanhSachTinhTrangSerializer(serializers.ModelSerializer):
    class Meta:
        model = TinhTrangPhongKham
        fields = '__all__'

class DanhSachPhongKhamSerializer(serializers.ModelSerializer):
    tinh_trang = DanhSachTinhTrangSerializer()
    class Meta:
        model = PhongKham
        fields = '__all__'

class TinhTrangPhongKhamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TinhTrangPhongKham
        fields = '__all__'

class PhongKhamSerializer(serializers.ModelSerializer):
    tinh_trang = TinhTrangPhongKhamSerializer()
    class Meta:
        model = PhongKham
        fields = '__all__'


# class BenhNhanBaoHiemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('ma_benh_nhan', 'ho_ten', 'ngay_sinh', 'gioi_tinh', 'dia_chi', 'ma_so_bao_hiem', 'ma_dkbd', 'gt_the_tu', 'gt_the_den', 'mien_cung_ct', )

class FilterChuoiKhamSerializer(serializers.ModelSerializer):
    ma_benh_nhan = serializers.CharField(source='benh_nhan.ma_benh_nhan')
    ho_ten = serializers.CharField(source='benh_nhan.ho_ten')
    ngay_sinh = serializers.CharField(source='benh_nhan.ngay_sinh')
    gioi_tinh = serializers.CharField(source='benh_nhan.gioi_tinh')
    dia_chi = serializers.CharField(source='benh_nhan.dia_chi')
    ma_the = serializers.CharField(source='benh_nhan.ma_so_bao_hiem')
    ma_dkbd = serializers.CharField(source='benh_nhan.ma_dkbd')
    gt_the_tu = serializers.CharField(source='benh_nhan.gt_the_tu')
    gt_the_den = serializers.CharField(source='benh_nhan.gt_the_den')
    mien_cung_ct = serializers.CharField(source='benh_nhan.mien_cung_ct')
    ly_do_vvien = serializers.CharField(source='lich_hen.ly_do_vvien')
    ma_benh = serializers.CharField(source='get_ma_benh')
    ten_benh = serializers.CharField(source='get_ten_benh')
    ngay_vao = serializers.CharField(source='lich_hen.thoi_gian_bat_dau')
    ngay_ra = serializers.CharField(source='lich_hen.thoi_gian_ket_thuc')
    so_ngay_dieu_tri = serializers.CharField(source='get_so_ngay_dieu_tri')
    ket_qua_dieu_tri = serializers.CharField(source='get_ket_qua_dieu_tri')
    ngay_ttoan = serializers.CharField(source='get_ngay_ttoan')
    t_thuoc = serializers.CharField(source='get_tien_thuoc')
    nam_qt = serializers.CharField(source='get_nam_qt')
    thang_qt = serializers.CharField(source='get_thang_qt')
    ma_loai_kcb = serializers.CharField(source='get_ma_loai_kcb')
    ma_khuvuc = serializers.CharField(source='benh_nhan.ma_khuvuc')
    ma_pttt_qt = serializers.CharField(source='get_ma_pttt_qt')
    can_nang = serializers.CharField(source='benh_nhan.can_nang')

    class Meta:
        model = ChuoiKham
        fields = (
            'ma_lk', 
            'ma_benh_nhan',
            'ho_ten', 
            'ngay_sinh',
            'gioi_tinh',
            'dia_chi',
            'ma_the', 
            'ma_dkbd',
            'gt_the_tu',
            'gt_the_den',
            'mien_cung_ct',  
            'ten_benh',
            'ma_benh',
            'ly_do_vvien',
            'ngay_vao',
            'ngay_ra',
            'so_ngay_dieu_tri', 
            'ket_qua_dieu_tri',
            'ngay_ttoan',
            't_thuoc',
            'nam_qt', 
            'thang_qt',
            'ma_loai_kcb',
            'ma_khuvuc',
            'ma_pttt_qt',
            'can_nang'
        )

class FilterDonThuocSerializer(serializers.ModelSerializer):
    ma_lk = serializers.CharField(source='don_thuoc.chuoi_kham.ma_lk')
    ma_thuoc = serializers.CharField(source='thuoc.ma_thuoc')
    ten_thuoc = serializers.CharField(source='thuoc.ten_thuoc')
    ma_nhom = serializers.CharField(source='thuoc.nhom_chi_phi.ma_nhom')
    don_vi_tinh = serializers.CharField(source='thuoc.don_vi_tinh')
    ham_luong = serializers.CharField(source='thuoc.ham_luong')
    duong_dung = serializers.CharField(source='thuoc.duong_dung')
    lieu_dung = serializers.CharField(source='ghi_chu')
    so_dang_ky = serializers.CharField(source='thuoc.so_dang_ky')
    tt_thau = serializers.CharField(source='thuoc.quyet_dinh')
    pham_vi = serializers.CharField(source='thuoc.pham_vi')
    tyle_tt = serializers.CharField(source='thuoc.tyle_tt')
    don_gia = serializers.CharField(source='thuoc.don_gia')
    thanh_tien = serializers.CharField(source='gia_ban')
    muc_huong = serializers.CharField(source='thuoc.muc_huong')
    t_nguonkhac = serializers.CharField(source='get_tt_nguon_khac')
    t_ngoaids = serializers.CharField(source='get_t_ngoaids')
    ngay_yl = serializers.CharField(source='get_ngay_yl')
    ma_pttt = serializers.CharField(source='get_ma_pttt')

    class Meta:
        model = KeDonThuoc
        fields = (
            'ma_lk',
            'ma_thuoc',
            'ma_nhom',
            'ten_thuoc',
            'don_vi_tinh',
            'ham_luong',
            'duong_dung',
            'lieu_dung',
            'so_dang_ky',
            'tt_thau',
            'pham_vi',
            'tyle_tt',
            'so_luong',
            'don_gia',
            'thanh_tien',
            'muc_huong',
            't_nguonkhac',
            't_ngoaids',
            'ngay_yl',
            'ma_pttt'
        )

class FilterDichVuSerializer(serializers.ModelSerializer):
    ma_lk = serializers.CharField(source='chuoi_kham.ma_lk')
    ma_dich_vu = serializers.CharField(source='dich_vu_kham.ma_dvkt')
    ma_vat_tu = serializers.CharField(source='get_ma_vat_tu')
    ma_nhom = serializers.CharField(source='dich_vu_kham.nhom_chi_phi.ma_nhom')
    ten_dich_vu = serializers.CharField(source='dich_vu_kham.ten_dvkt')
    so_luong = serializers.CharField(source='get_so_luong')
    don_gia = serializers.CharField(source='dich_vu_kham.don_gia')
    tyle_tt = serializers.CharField(source='dich_vu_kham.tyle_tt')
    thanh_tien = serializers.CharField(source='dich_vu_kham.don_gia')
    ma_benh = serializers.CharField(source='chuoi_kham.get_ma_benh')
    ngay_yl = serializers.CharField(source='get_ngay_yl')
    ngay_kq = serializers.CharField(source='get_ngay_kq')
    t_nguonkhac = serializers.CharField(source='get_t_nguonkhac')
    t_ngoaids = serializers.CharField(source='get_t_ngoaids')
    ma_pttt = serializers.CharField(source='get_ma_pttt')

    class Meta:
        model = PhanKhoaKham
        fields = (
            'ma_lk',
            'ma_dich_vu',
            'ma_vat_tu',
            'ma_nhom',
            'ten_dich_vu',
            'so_luong',
            'don_gia',
            'tyle_tt',
            'thanh_tien',
            't_nguonkhac',
            't_ngoaids',
            'ma_benh',
            'ngay_yl',
            'ngay_kq',
            'ma_pttt'
        )

class MauPhieuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MauPhieu
        fields = '__all__'

class TatCaLichHenSerializer(serializers.ModelSerializer):
    trang_thai = TrangThaiLichHenSerializer()
    class Meta:
        model = LichHenKham
        fields = ('id', 'ma_lich_hen', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'trang_thai')

class FilterHoaDonChuoiKhamBaoHiemSerializer(serializers.ModelSerializer):
    benh_nhan = serializers.CharField(source='chuoi_kham.benh_nhan.ho_ten')
    nam_sinh = serializers.CharField(source='chuoi_kham.benh_nhan.ngay_sinh')
    gioi_tinh = serializers.CharField(source='chuoi_kham.benh_nhan.gioi_tinh')
    ma_bhyt = serializers.CharField(source='chuoi_kham.benh_nhan.ma_so_bao_hiem')
    ma_dkbd = serializers.CharField(source='chuoi_kham.benh_nhan.ma_dkbd')
    ma_benh = serializers.CharField(source='get_ma_benh')
    tong_cong_1 = serializers.CharField(source='get_tong_cong')
    tien_kham = serializers.CharField(source='get_tong_cong')
    tu_chi_tra = serializers.CharField(source='tong_tien')
    tong_cong_2 = serializers.CharField(source='get_tong_cong_2')

    class Meta:
        model = HoaDonChuoiKham
        fields = (
            'benh_nhan',
            'gioi_tinh',
            'nam_sinh',
            'ma_bhyt',
            'ma_dkbd',
            'ma_benh',
            'tong_cong_1',
            'tien_kham',
            'tu_chi_tra',
            'tong_cong_2'
        )

class DanhSachKetQuaChuoiKhamSerializer(serializers.ModelSerializer):
    benh_nhan = UserSerializerSimple()
    trang_thai = TrangThaiChuoiKhamSerializer()
    class Meta:
        model = ChuoiKham
        fields = '__all__'

class DanhSachThuocSerializerSimple(serializers.ModelSerializer):
    thuoc = ThuocSerializerSimple()
    class Meta:
        model = KeDonThuoc
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'

class ChiTietChiSoXetNghiemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChiTietChiSoXetNghiem
        fields = '__all__'

class ChiSoXetNghiemSerializer(serializers.ModelSerializer):
    chi_tiet = ChiTietChiSoXetNghiemSerializer()
    class Meta:
        model = ChiSoXetNghiem
        fields = '__all__'

class KetQuaXetNghiemSerializer(serializers.ModelSerializer):
    # chi_so_xet_nghiem = ChiSoXetNghiemSerializer()
    dich_vu = serializers.CharField(source='get_ten_dvkt')
    chi_so_xet_nghiem = ChiSoXetNghiemSerializer()
    class Meta:
        model = KetQuaXetNghiem
        fields = (
            'dich_vu',
            'chi_so_xet_nghiem',
            'ket_qua_xet_nghiem',
            'danh_gia_chi_so',
            'danh_gia_ghi_chu',

        )

class PhieuKetQuaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HtmlKetQua
        fields = '__all__'