from finance.models import HoaDonChuoiKham, HoaDonThuoc, HoaDonLamSang
from medicine.serializers import CongTySerializer, ThuocSerializer
# from finance.serializers import HoaDonChuoiKhamSerializer, HoaDonThuocSerializer
from os import set_inheritable
from django.http.request import validate_host
from rest_framework import fields, serializers
from django.contrib.auth import get_user_model
from .models import (
    BaiDang, 
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
    ProfilePhongChucNang, 
    TrangThaiChuoiKham, 
    TrangThaiKhoaKham, 
    TrangThaiLichHen, 
    ChuoiKham, 
    BacSi,
    TinhTrangPhongKham,
)
from medicine.models import DonThuoc, NhomVatTu, VatTu

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
    class Meta:
        model = KetQuaChuyenKhoa
        fields = ('id', 'ma_ket_qua', 'mo_ta', 'ket_luan', 'file_chuyen_khoa')

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