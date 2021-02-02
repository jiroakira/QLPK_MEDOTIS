
import decimal
import hashlib
import datetime
import os
from bulk_update_or_create.query import BulkUpdateOrCreateQuerySet
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.core.files.storage import FileSystemStorage
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def file_url(self, filename): 

    hash_ = hashlib.md5()
    hash_.update(str(filename).encode("utf-8") + str(datetime.datetime.now()).encode("utf-8"))
    file_hash = hash_.hexdigest()
    filename = filename
    return "%s%s/%s" % (self.file_prepend, file_hash, filename)

class UserManager(BaseUserManager):
    def create_user(self, ho_ten, so_dien_thoai, cmnd_cccd, dia_chi, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not so_dien_thoai:
            raise ValueError('Users must have an mobile number')

        if not ho_ten:
            raise ValueError('Users must have their name')

        user = self.model(
            so_dien_thoai=so_dien_thoai,
            ho_ten = ho_ten,
            cmnd_cccd = cmnd_cccd,
            dia_chi = dia_chi,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_nguoi_dung(self, ho_ten, so_dien_thoai, cmnd_cccd, gioi_tinh, dan_toc, ngay_sinh, ma_so_bao_hiem, dia_chi, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not so_dien_thoai:
            raise ValueError('Users must have an mobile number')

        if not ho_ten:
            raise ValueError('Users must have their name')

        user = self.model(
            so_dien_thoai  = so_dien_thoai,
            ho_ten         = ho_ten,
            cmnd_cccd      = cmnd_cccd,
            dia_chi        = dia_chi,
            gioi_tinh      = gioi_tinh,
            dan_toc        = dan_toc,
            ngay_sinh      = ngay_sinh,
            ma_so_bao_hiem = ma_so_bao_hiem
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, ho_ten, so_dien_thoai, cmnd_cccd, dia_chi, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            so_dien_thoai=so_dien_thoai,
            password=password,
            ho_ten=ho_ten,
            cmnd_cccd = cmnd_cccd,
            dia_chi = dia_chi,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, ho_ten, so_dien_thoai, cmnd_cccd, dia_chi, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            so_dien_thoai=so_dien_thoai,
            password=password,
            ho_ten=ho_ten,
            cmnd_cccd = cmnd_cccd,
            dia_chi = dia_chi,
        )
        
        user.staff = True
        user.admin = True
        user.chuc_nang = 7
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    file_prepend = 'user/img/'
    GENDER = (
        ('1', "Nam"),
        ('2', "Nữ"),
        ('3', "Không xác định"),
    )
    ROLE = (
        ('1', 'Người Dùng'),
        ('2', 'Lễ Tân'),
        ('3', 'Bác Sĩ Lâm Sàng'),
        ('4', 'Bác Sĩ Chuyên Khoa'),
        ('5', 'Nhân Viên Phòng Tài Chính'),
        ('6', 'Nhân Viên Phòng Thuốc'),
        ('7', 'Quản Trị Viên')
    )
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    ma_benh_nhan = models.CharField(max_length=20, unique=True, null=True)
    phone_regex = RegexValidator(regex=r"(84|0[3|5|7|8|9])+([0-9]{8})\b")
    so_dien_thoai = models.CharField(max_length=10, unique=True, validators=[phone_regex])
    ho_ten = models.CharField(max_length = 255)

    email = models.EmailField(null=True, unique=True, blank=True)
    cmnd_cccd = models.CharField(max_length=13, null=True, unique = True)
    ngay_sinh = models.DateField(null=True, blank=True)
    gioi_tinh = models.CharField(choices=GENDER, max_length = 10, null=True, blank=True)

    can_nang = models.PositiveIntegerField(null=True, blank=True)

    anh_dai_dien = models.FileField(max_length=1000, upload_to=file_url, null=True, blank=True)
    dia_chi = models.TextField(max_length=1000, null=True, blank=True)
    dan_toc = models.CharField(max_length=40, null=True, blank=True)
    chuc_nang = models.CharField(choices=ROLE, max_length = 1, default='1')
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that is built in.
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='child')
    ma_so_bao_hiem = models.CharField(max_length=25, null=True, blank=True)
    ma_dkbd = models.CharField(max_length=10, null=True, blank=True)
    ma_khuvuc = models.CharField(max_length=10, null=True, blank=True)
    gt_the_tu = models.DateField(null=True, blank=True)
    gt_the_den = models.DateField(null=True, blank=True)
    mien_cung_ct = models.DateField(null=True, blank=True)
    muc_huong = models.PositiveIntegerField(null=True, blank=True)

    so_diem_tich = models.PositiveIntegerField(null=True, blank=True)

    thoi_gian_tao = models.DateTimeField(editable=False, null=True, blank=True)
    thoi_gian_cap_nhat = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.thoi_gian_tao = timezone.now()
            now = timezone.now()
            date_time = now.strftime("%m%d%y%H%M%S")
            self.ma_benh_nhan = date_time
        self.thoi_gian_cap_nhat = timezone.now()
        return super(User, self).save(*args, **kwargs)

    objects = UserManager()

    USERNAME_FIELD = 'so_dien_thoai'
    REQUIRED_FIELDS = ['ho_ten', 'cmnd_cccd', 'dia_chi',] # Email & Password are required by default.

    def __str__(self):       
        return self.ho_ten

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    def getSubName(self):
        lstChar = []
        lstString = self.ho_ten.split(' ')
        for i in lstString:
            lstChar.append(i[0].upper())
        subName = "".join(lstChar)
        return subName

    def tuoi(self):
        now = datetime.date.today()
        days = now - self.ngay_sinh
        return int((days.days / 365))
        
class BacSi(models.Model):
    Type = (
        ('full_time', "Full-Time"),
        ('part_time', "Part-Time"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    chung_chi_hanh_nghe = models.CharField(max_length=50, null=True, blank=True)
    gioi_thieu = models.TextField(null=True, blank=True)
    chuc_danh = models.CharField(max_length=255, null=True, blank=True)
    chuyen_khoa = models.CharField(max_length=255, null=True, blank=True)
    noi_cong_tac = models.TextField(null=True, blank=True)
    kinh_nghiem = models.TextField(null=True, blank=True)
    loai_cong_viec = models.CharField(null=True, blank=True, choices= Type, max_length=50)

    class Meta:
        verbose_name = "Bác Sĩ"
        verbose_name_plural = "Bác Sĩ"

class TinhTrangPhongKham(models.Model):
    """ Mở rộng phần tình trạng của phòng khám, khi phòng khám muốn tạm ngưng hoạt động
    trong một khoảng thời gian thì bảng này sẽ được sử dụng để mở rộng tính năng cho bảng Phòng Khám """
    kha_dung = models.BooleanField(default=True)
    thoi_gian_dong_cua = models.DateTimeField(null=True, blank=True)
    thoi_gian_mo_cua = models.DateTimeField(null=True, blank=True)

    # tọa độ địa lí của phòng khám sẽ được sử dụng để hiển thị lên map trong mobile app
    latitude = models.CharField(null=True, blank=True, max_length=50)
    longtitude = models.CharField(null=True, blank=True, max_length=50)
    
class PhongKham(models.Model):
    """ Thông tin chi tiết của phòng khám """
    file_prepend = "logo_phong_kham/"

    ma_cskcb = models.CharField(max_length=10, null=True, blank=True)

    ten_phong_kham = models.CharField(max_length = 255)
    dia_chi = models.TextField(null=True, blank=True)
    so_dien_thoai = models.CharField(max_length = 12)
    email = models.EmailField(null=True, blank=True)
    logo = models.FileField(upload_to = file_url, null=True, blank=True)
    tinh_trang = models.ForeignKey(TinhTrangPhongKham, on_delete=models.CASCADE)
    gia_tri_diem_tich = models.PositiveIntegerField(null=True, blank=True)
    # NEW 
    chu_khoan = models.CharField(max_length=255, null=True, blank=True)
    so_tai_khoan = models.CharField(max_length=20, null=True, blank=True)
    thong_tin_ngan_hang = models.TextField(null=True, blank=True)
    # END
    class Meta:
        verbose_name = "Phòng Khám"
        verbose_name_plural = "Phòng Khám"

class PhongChucNang(models.Model):
    """ Mỗi dịch vụ khám sẽ có một phòng chức năng riêng biệt, là nơi bệnh nhân sau khi được phân dịch vụ khám sẽ đến trong suốt chuỗi khám của bệnh nhân """
    ten_phong_chuc_nang = models.CharField(max_length=255)
    bac_si_phu_trach = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="bac_si_chuyen_khoa")
    # dich_vu_kham = models.ForeignKey(DichVuKham, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="phong_chuc_nang_theo_dich_vu")
    thoi_gian_tao = models.DateTimeField(editable=False, null=True, blank=True, auto_now_add=True)
    thoi_gian_cap_nhat = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    class Meta:
        verbose_name = "Phòng Chức Năng"
        verbose_name_plural = "Phòng Chức Năng"

    def __str__(self):
        return self.ten_phong_chuc_nang
    
    def danh_sach_benh_nhan_theo_dich_vu_kham(self):
        # return self.dich_vu_kham.dich_vu_kham.all()
        return self.ten_phong_chuc_nang
    # def save(self, *agrs, **kwargs):
    #     if not self.id:
    #         self.thoi_gian_tao = timezone.now
    #     self.thoi_gian_cap_nhat = timezone.now
    #     return super(PhongChucNang, self).save(*agrs, **kwargs)

    # TODO review table PhongChucNang again

class DichVuKham(models.Model):
    """ Danh sách tất cả các dịch vụ khám trong phòng khám """
    khoa = models.ForeignKey("DanhMucKhoa", on_delete=models.SET_NULL, null=True, blank=True)

    ma_dvkt = models.CharField(max_length=50, null=True, blank=True)
    stt = models.CharField(max_length=10, null=True, blank=True, unique=True)
    ten_dvkt = models.CharField(max_length=255, null=True, blank=True)
    ma_gia = models.CharField(max_length=50, null=True, blank=True)
    don_gia = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=0)
    quyet_dinh = models.CharField(max_length=10, null=True, blank=True)
    cong_bo = models.CharField(max_length=10, null=True, blank=True)
    ma_cosokcb = models.CharField(max_length=20, null=True, blank=True)
    ten_dich_vu = models.CharField(max_length=255, null=True, blank=True)
    bao_hiem = models.BooleanField(default=False)

    nhom_chi_phi = models.ForeignKey('NhomChiPhi', on_delete=models.SET_NULL, null=True, blank=True)
    tyle_tt = models.IntegerField(null=True, blank=True)
    # bac_si_phu_trach = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="bac_si_phu_trach", null=True, blank=True)
    # khoa_kham = models.ForeignKey(KhoaKham, on_delete=models.SET_NULL, related_name="khoa_kham", null=True, blank=True)
    phong_chuc_nang = models.ForeignKey(PhongChucNang, on_delete=models.SET_NULL, null=True, blank=True, related_name="dich_vu_kham_theo_phong")

    chi_so = models.BooleanField(default=False)
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    class Meta:
        verbose_name = "Dịch Vụ Khám"
        verbose_name_plural = "Dịch Vụ Khám"

    def __str__(self):
        return self.ten_dvkt

    @property
    def check_chi_so(self):
        if self.chi_so == True:
            return True
        else:
            return False
class GiaDichVu(models.Model):
    """ Bảng giá sẽ lưu trữ tất cả giá của dịch vụ khám và cả thuốc """
    id_dich_vu_kham = models.OneToOneField(DichVuKham, null=True, blank=True, on_delete=models.PROTECT, related_name="gia_dich_vu_kham")
    gia = models.DecimalField(max_digits=10, decimal_places=3)  
    # id_thuoc = models.ForeignKey(Thuoc, on_delete=models.PROTECT, null=True, blank=True, related_name="gia_thuoc")
    thoi_gian_tao = models.DateTimeField(null=True, blank=True, editable=False)
    thoi_gian_chinh_sua = models.DateTimeField(null=True, blank=True)

    def save(self, *agrs, **kwargs):
        if not self.id:
            self.thoi_gian_tao = timezone.now()
        self.thoi_gian_chinh_sua = timezone.now()
        return super(GiaDichVu, self).save(*agrs, **kwargs)

class BaoHiem(models.Model):
    """ Bảng Bảo Hiểm sẽ lưu trữ tất cả các loại bảo hiểm áp dụng trong phòng khám """
    ten_bao_hiem = models.CharField(max_length=255)
    # dạng bảo hiểm ở đây là số % được bảo hiểm chi trả
    dang_bao_hiem = models.SmallIntegerField(null=True, blank=True)
    id_dich_vu_kham = models.OneToOneField(DichVuKham, null=True, blank=True, on_delete=models.PROTECT, related_name="bao_hiem_dich_vu_kham")
    # id_thuoc = models.ForeignKey(Thuoc, on_delete=models.PROTECT, null=True, blank=True, related_name="bao_hiem_thuoc")
    thoi_gian_tao = models.DateTimeField()
    thoi_gian_chinh_sua = models.DateTimeField()

    def save(self, *agrs, **kwargs):
        if not self.id:
            self.thoi_gian_tao = timezone.now()
        self.thoi_gian_chinh_sua = timezone.now()
        return super(BaoHiem, self).save(*agrs, **kwargs)

class ProfilePhongChucNang(models.Model):
    phong_chuc_nang = models.OneToOneField(PhongChucNang, on_delete=models.CASCADE, related_name="profile_phong_chuc_nang")
    so_luong_cho = models.PositiveIntegerField(null=True, blank=True)
    thoi_gian_trung_binh = models.PositiveIntegerField(help_text="Đơn vị(phút)", null=True, blank=True)
    status = models.BooleanField(default=True)

@receiver(post_save, sender=PhongChucNang)
def create_or_update_func_room_profile(sender, instance, created, **kwargs):
    if created:
        ProfilePhongChucNang.objects.create(phong_chuc_nang=instance)
    instance.profile_phong_chuc_nang.save()

def get_sentinel_user():
    return User.objects.get_or_create(ho_ten='deleted')[0]

class TrangThaiLichHen(models.Model):
    ten_trang_thai = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Trạng Thái Lịch Hẹn"
        verbose_name_plural = "Trạng Thái Lịch Hẹn"

    def __str__(self):
        return f"({self.id})" + self.ten_trang_thai 

def get_default_trang_thai_lich_hen():
    return TrangThaiLichHen.objects.get_or_create(ten_trang_thai="Đã đặt trước")[0]

from datetime import timedelta

today = timezone.localtime(timezone.now())
tomorrow = today + timedelta(1)
today_start = today.replace(hour=0, minute=0, second=0)
today_end = tomorrow.replace(hour=0, minute=0, second=0)

# class LichHenKhamManager(models.Manager):
#     def lich_hen_hom_nay(self):
#         return self.filter(thoi_gian_bat_dau__lte = today_end, thoi_gian_ket_thuc__gte = today_start)
class LichHenKham(models.Model):

    LYDO_VVIEN = (
        ("1", "Đúng Tuyến"),
        ("2", "Cấp Cứu"),
        ("3", "Trái Tuyến"),
        ("4", "Thông Tuyến"),
    )

    LOAI_DICH_VU = (
        ('kham_chua_benh', 'Khám Chữa Bệnh'),
        ('kham_suc_khoe', 'Khám Sức Khỏe')
    )


    ma_lich_hen = models.CharField(max_length=15, null=True, blank=True)
    benh_nhan = models.ForeignKey(User, on_delete=models.CASCADE, related_name="benh_nhan_hen_kham")
    nguoi_phu_trach = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="nguoi_phu_trach")

    thoi_gian_bat_dau = models.DateTimeField()
    thoi_gian_ket_thuc = models.DateTimeField(null=True, blank=True)
    ly_do = models.TextField(null=True, blank=True)
    dia_diem = models.CharField(max_length=255, null=True, blank=True)
    loai_dich_vu = models.CharField(choices=LOAI_DICH_VU, null=True, blank=True, max_length=25)
    trang_thai = models.ForeignKey(TrangThaiLichHen, on_delete=models.CASCADE, null=True, blank=True)

    ly_do_vvien = models.CharField(max_length=5, choices=LYDO_VVIEN, null=True, blank=True)

    thoi_gian_tao = models.DateTimeField(editable=False, null=True, blank=True, auto_now_add=True)
    thoi_gian_chinh_sua = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = "Lịch Hẹn Khám"
        verbose_name_plural = "Lịch Hẹn Khám"

    def save(self, *args, **kwargs):
        if not self.id:
            now = timezone.now()
            date_time = now.strftime("%m%d%y%H%M%S")
            ma_lich_hen = "LH" + date_time
            self.ma_lich_hen = ma_lich_hen
        return super(LichHenKham, self).save(*args, **kwargs)

    

    # objects = LichHenKhamManager()


class LichSuTrangThaiLichHen(models.Model):
    lich_hen_kham = models.ForeignKey(LichHenKham, on_delete=models.CASCADE, related_name="lich_hen")
    trang_thai_lich_hen = models.ForeignKey(TrangThaiLichHen, on_delete=models.CASCADE, related_name="trang_thai_lich_hen")
    # Nêu rõ nguyên nhân dẫn đến trạng thái đó
    chi_tiet_trang_thai = models.CharField(max_length=500, null=True, blank=True)

    thoi_gian_tao = models.DateTimeField(auto_now_add=True)

def get_sentinel_dich_vu():
    return DichVuKham.objects.get_or_create(ten_dich_vu='deleted')[0]

class TrangThaiKhoaKham(models.Model):
    """ Tất cả các trạng thái có thể xảy ra trong phòng khám """
    trang_thai_khoa_kham = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Trạng Thái Khoa Khám"
        verbose_name_plural = "Trạng Thái Khoa Khám"

    def __str__(self):
        return f"({self.id})" + self.trang_thai_khoa_kham 

class TrangThaiChuoiKham(models.Model):
    trang_thai_chuoi_kham = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Trạng Thái Chuỗi Khám"
        verbose_name_plural = "Trạng Thái Chuỗi Khám"

    def __str__(self):
        return f"({self.id})" + self.trang_thai_chuoi_kham

def get_default_trang_thai_chuoi_kham():
    return TrangThaiChuoiKham.objects.get_or_create(trang_thai_chuoi_kham="Đang chờ")[0]

def get_default_trang_thai_khoa_kham():
    return TrangThaiKhoaKham.objects.get_or_create(trang_thai_khoa_kham="Đang chờ")[0]

class ChuoiKham(models.Model):
    """ Mỗi bệnh nhân khi tới phòng khám để sau khi khám tổng quát thì đều sẽ có một chuỗi khám.
    Do chuỗi khám này có tính tích lũy nên bệnh nhân có thể dễ dàng xem lại được lịch sử khám của mình kết hợp với các kết quả khám tại phòng khám """
    ma_lk = models.CharField(max_length=100, null=True, blank=True)
    benh_nhan = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name="chuoi_kham")
    bac_si_dam_nhan = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name="bac_si_chuoi_kham", null=True, blank=True)
    lich_hen = models.ForeignKey(LichHenKham, on_delete=models.SET_NULL, null=True, blank=True, related_name='danh_sach_chuoi_kham')
    thoi_gian_bat_dau = models.DateTimeField(null=True, blank=True)
    thoi_gian_ket_thuc = models.DateTimeField(null=True, blank=True)
    thoi_gian_tai_kham = models.DateTimeField(null=True, blank=True)
    trang_thai = models.ForeignKey(TrangThaiChuoiKham, on_delete=models.CASCADE, related_name="trang_thai", null=True, blank=True)

    thoi_gian_tao = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    thoi_gian_cap_nhat = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "Chuỗi Khám"
        verbose_name_plural = "Chuỗi Khám"

    def get_ma_benh(self):
        return self.ket_qua_tong_quat.all()[0].ma_benh.ma_benh

    def get_ten_benh(self):
        return self.ket_qua_tong_quat.all()[0].ma_benh.ten_benh

    def get_so_ngay_dieu_tri(self):
        if (self.thoi_gian_ket_thuc - self.thoi_gian_bat_dau).days == 0:
            return "1"
        else:
            return (self.thoi_gian_ket_thuc - self.thoi_gian_bat_dau).days
    
    def get_ket_qua_dieu_tri(self):
        return self.ket_qua_tong_quat.all()[0].ket_qua_dieu_tri

    def get_ngay_ttoan(self):
        return self.hoa_don_dich_vu.thoi_gian_tao.strftime("%Y%m%d%H%M")
    
    def get_tien_thuoc(self):
        return self.don_thuoc_chuoi_kham.all()[0].hoa_don_thuoc.tong_tien

    def get_nam_qt(self):
        return self.hoa_don_dich_vu.thoi_gian_tao.strftime("%Y")

    def get_thang_qt(self):
        return self.hoa_don_dich_vu.thoi_gian_tao.strftime("%m")

    def get_ma_loai_kcb(self):
        return '1'

    def get_ma_pttt_qt(self):
        return ""


class PhanKhoaKham(models.Model):
    benh_nhan = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    dich_vu_kham = models.ForeignKey(DichVuKham, on_delete=models.SET_NULL, null=True, blank=True, related_name="phan_khoa_dich_vu")
    bac_si_lam_sang = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name="bac_si")
    chuoi_kham = models.ForeignKey(ChuoiKham, on_delete=models.CASCADE, null=True, blank=True, related_name="phan_khoa_kham")
    bao_hiem = models.BooleanField(default=False)
    priority = models.SmallIntegerField(null=True, blank=True)

    thoi_gian_bat_dau = models.DateTimeField(null=True, blank=True)
    thoi_gian_ket_thuc = models.DateTimeField(null=True, blank=True)

    trang_thai = models.ForeignKey(TrangThaiKhoaKham, on_delete=models.SET_NULL, null=True)

    thoi_gian_tao = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    thoi_gian_cap_nhat = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = "Phân Khoa Khám"
        verbose_name_plural = "Phân Khoa Khám"

    

    def gia_dich_vu_theo_bao_hiem(self):
        gia = self.dich_vu_kham.gia_dich_vu_kham.gia 
        if self.bao_hiem:
            tong_tien = gia * decimal.Decimal((1 - (self.dich_vu_kham.bao_hiem_dich_vu_kham.dang_bao_hiem / 100)))
        else:
            tong_tien = gia
        return tong_tien

    def gia(self):
        return self.dich_vu_kham.gia_dich_vu_kham.gia 

    def muc_bao_hiem(self):
        return self.dich_vu_kham.bao_hiem_dich_vu_kham.dang_bao_hiem

    def get_ma_vat_tu(self):
        return ""

    def get_so_luong(self):
        return '1'

    def get_ngay_yl(self):
        return self.thoi_gian_bat_dau.strftime("%Y%m%d%H%M")

    def get_ngay_kq(self):
        return self.thoi_gian_ket_thuc.strftime("%Y%m%d%H%M")

    def get_t_nguonkhac(self):
        return 0
    
    def get_t_ngoaids(self):
        return 0

    def get_ma_pttt(self):
        return 1
    

@receiver(post_save, sender=PhanKhoaKham)
def send_func_room_info(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"funcroom_service", {
                'type': 'funcroom_info'
            }
        )

class LichSuTrangThaiKhoaKham(models.Model):
    phan_khoa_kham = models.ForeignKey(PhanKhoaKham, on_delete=models.CASCADE, null=True, blank=True)
    trang_thai_khoa_kham = models.ForeignKey(TrangThaiKhoaKham, on_delete=models.CASCADE, null=True, blank=True)
    # Nêu rõ nguyên nhân dẫn tới trạng thái đó
    chi_tiet_trang_thai = models.CharField(max_length=500, null=True, blank=True)
    
    thoi_gian_tao = models.DateTimeField(auto_now_add=True)

class LichSuChuoiKham(models.Model):
    chuoi_kham = models.ForeignKey(ChuoiKham, on_delete=models.CASCADE, null=True, blank=True)
    trang_thai = models.ForeignKey(TrangThaiChuoiKham, on_delete=models.CASCADE, null=True, blank=True)
    # Nêu rõ nguyên nhân dẫn tới trạng thái đó
    chi_tiet_trang_thai = models.CharField(max_length=500, null=True, blank=True)
    
    thoi_gian_tao = models.DateTimeField(auto_now_add=True)

class KetQuaTongQuat(models.Model):
    """ Kết quả tổng quát của người dùng sau một lần đến thăm khám tại phòng khám """
    RESULT_CHOICES = (
        ("1", "Khỏi"),
        ("2", "Đỡ"), 
        ("3", "Không Thay Đổi"),
        ("4", "Nặng Hơn"),
        ("5", "Tử Vong"),
    )

    chuoi_kham = models.ForeignKey(ChuoiKham, on_delete=models.SET_NULL, null=True, related_name="ket_qua_tong_quat")
    # benh_nhan = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    ma_benh = models.ForeignKey('DanhMucBenh', on_delete=models.SET_NULL, null=True, blank=True)
    ma_ket_qua = models.CharField(max_length=50, null=True, blank=True)
    mo_ta = models.CharField(max_length=255, null=True, blank=True)
    ket_luan = models.TextField(null=True, blank=True)

    ket_qua_dieu_tri = models.CharField(max_length=5, choices=RESULT_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "Kết Quả Tổng Quát"
        verbose_name_plural = "Kết Quả Tổng Quát"

class KetQuaChuyenKhoa(models.Model):
    """ Kết quả của khám chuyên khoa mà người dùng có thể nhận được """ 
    ma_ket_qua = models.CharField(max_length=50, null=True, blank=True, unique=True)
    phan_khoa_kham = models.ForeignKey(PhanKhoaKham, on_delete=models.CASCADE, null=True, blank=True, related_name="ket_qua_chuyen_khoa")
    ket_qua_tong_quat = models.ForeignKey(KetQuaTongQuat, on_delete=models.CASCADE, related_name="ket_qua_chuyen_khoa")
    mo_ta = models.CharField(max_length=255, null=True, blank=True)
    ket_luan = models.TextField(null=True, blank=True)

    chi_so = models.BooleanField(default = False)

    class Meta:
        verbose_name = "Kết Quả Chuyên Khoa"
        verbose_name_plural = "Kết Quả Chuyên Khoa"

key_store = FileSystemStorage()

class FileKetQua(models.Model):
    """ File kết quả của mỗi người dùng """
    file_prepend = 'user/documents/'
    file = models.FileField(upload_to=file_url,null=True, blank=True, storage=key_store)
    # file = models.CharField(max_length=500, null=True, blank=True)
    thoi_gian_tao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tài Liệu"
        verbose_name_plural = "Tài Liệu"
    
    def __unicode__(self):
        return self.file.url

    def filename(self):
        return os.path.basename(self.file.name)
    # ket_qua_chuyen_khoa = models.ForeignKey(KetQuaChuyenKhoa, on_delete=models.SET_NULL, null=True, blank=True, related_name="file_ket_qua_chuyen_khoa")
    # ket_qua_tong_quat = models.ForeignKey(KetQuaTongQuat, on_delete=models.SET_NULL, null=True, blank=True, related_name="file_ket_qua_tong_quat")

class FileKetQuaTongQuat(models.Model):
    file = models.ForeignKey(FileKetQua, on_delete=models.CASCADE, related_name="file_tong_quat")
    ket_qua_tong_quat = models.ForeignKey(KetQuaTongQuat, on_delete=models.CASCADE, related_name="file_ket_qua_tong_quat")

    class Meta:
        verbose_name = "File Kết Quả Tổng Quát"
        verbose_name_plural = "File Kết Quả Tổng Quát"

class FilePhongKham(models.Model):
    file_prepend = 'phongkham/documents/'
    file = models.FileField(upload_to=file_url, null=True, blank=True, storage=key_store)

    thoi_gian_tao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tài Liệu Phòng Khám"
        verbose_name_plural = "Tài Liệu Phòng Khám"


class FileKetQuaChuyenKhoa(models.Model):
    file = models.ForeignKey(FileKetQua, on_delete=models.CASCADE, related_name="file_chuyen_khoa")
    ket_qua_chuyen_khoa = models.ForeignKey(KetQuaChuyenKhoa, on_delete=models.CASCADE, related_name="file_ket_qua_chuyen_khoa")

    class Meta:
        verbose_name = "File Kết Quả Chuyên Khoa"
        verbose_name_plural = "File Kết Quả Chuyên Khoa"

class BaiDang(models.Model):
    file_prepend = 'bai_dang/'
    tieu_de = models.TextField(null=True, blank=True)
    hinh_anh = models.ImageField(upload_to = file_url, null=True, blank=True)
    noi_dung_chinh = models.TextField(null=True, blank=True)
    noi_dung = models.TextField(null=True, blank=True)
    thoi_gian_bat_dau = models.DateTimeField(null=True, blank=True)
    thoi_gian_ket_thuc = models.DateTimeField(null=True, blank=True)
    nguoi_dang_bai = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="nguoi_dang_bai", null=True, blank=True)

    thoi_gian_tao = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = "Bài Đăng"
        verbose_name_plural = "Bài Đăng"


# * ------ Update 19/01 -------

class ChiSoXetNghiem(models.Model):
    dich_vu_kham = models.ForeignKey(DichVuKham, on_delete=models.CASCADE, null=True, blank=True, related_name="chi_so_xet_nghiem")
    doi_tuong_xet_nghiem = models.ForeignKey("DoiTuongXetNghiem", on_delete=models.SET_NULL, null=True, blank=True)
    ma_chi_so = models.CharField(max_length=10, null=True, blank=True)
    ten_chi_so = models.CharField(max_length=255, null=True, blank=True)
    chi_tiet = models.ForeignKey("ChiTietChiSoXetNghiem", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Chỉ Số Xét Nghiệm"
        verbose_name_plural = "Chỉ Số Xét Nghiệm"

    # def __str__(self):
    #     return f"({self.ma_chi_so}){self.ten_chi_so}/{self.doi_tuong_xet_nghiem}"

class ChiTietChiSoXetNghiem(models.Model):
    chi_so_binh_thuong_min = models.CharField(null=True, blank=True, max_length=10)
    chi_so_binh_thuong_max = models.CharField(null=True, blank=True, max_length=10)
    chi_so_binh_thuong = models.CharField(null=True, blank=True, max_length=10)
    don_vi_do = models.CharField(max_length=50, null=True, blank=True)
    ghi_chu = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Chi Tiết Chỉ Số Xét Nghiệm"
        verbose_name_plural = "Chi Tiết Chỉ Số Xét Nghiệm"

    def __str__(self):
        if not self.chi_so_binh_thuong:
            return f"({self.chi_so_binh_thuong_min}-{self.chi_so_binh_thuong_max})-{self.ghi_chu}"
        elif not self.chi_so_binh_thuong_min and self.chi_so_binh_thuong_max:
            return f"{self.chi_so_binh_thuong}"

    @property
    def check_chi_so_binh_thuong(self):
        if not self.chi_so_binh_thuong:
            return False
        else:
            return True

class DoiTuongXetNghiem(models.Model):
    MALE = "1"
    FEMALE = "2"
    UNDEFINED = "3"
    gender_choices = (
        (MALE, "Nam"),
        (FEMALE, "Nữ"),
        (UNDEFINED, "Chưa Xác Định"),
    )
    gioi_tinh = models.CharField(choices=gender_choices, max_length=5, null=True, blank=True)
    do_tuoi = models.ForeignKey('DoTuoiXetNghiem', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Đối Tượng Xét Nghiệm"
        verbose_name_plural = "Đối Tượng Xét Nghiệm"

    def __str__(self):
        if self.gioi_tinh == "1":        
            return f"Nam({self.do_tuoi})"
        elif self.gioi_tinh == "2":
            return f"Nữ({self.do_tuoi})"
        else:
            return f"Không Xác Định({self.do_tuoi})"
    
class DoTuoiXetNghiem(models.Model):
    do_tuoi_min = models.PositiveIntegerField(null=True, blank=True)
    do_tuoi_max = models.PositiveIntegerField(null=True, blank=True)
    ghi_chu = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Độ Tuổi Xét Nghiệm"
        verbose_name_plural = "Độ Tuổi Xét Nghiệm"

    def __str__(self):
        if not self.do_tuoi_min:
            return "< " + str(self.do_tuoi_max)
        elif not self.do_tuoi_max:
            return "> " + str(self.do_tuoi_min)
        else:
            return str(self.do_tuoi_min) + "-" + str(self.do_tuoi_max)

class KetQuaXetNghiem(models.Model):
    OK = "1"
    NG = "0"
    judment_choices = (
        (OK, "Bình thường"),
        (NG, "Bất bình thường"),
    )
    phan_khoa_kham = models.ForeignKey(PhanKhoaKham, on_delete=models.CASCADE, null=True, blank=True)
    ket_qua_chuyen_khoa = models.ForeignKey(KetQuaChuyenKhoa, on_delete=models.CASCADE, null=True, blank=True, related_name="ket_qua_xet_nghiem")
    chi_so_xet_nghiem = models.ForeignKey(ChiSoXetNghiem, on_delete=models.SET_NULL, null=True, blank=True)
    ket_qua_xet_nghiem = models.CharField(max_length=50, null=True, blank=True)
    danh_gia_chi_so = models.CharField(choices=judment_choices, max_length=5, null=True, blank=True)
    danh_gia_ghi_chu = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Kết Quả Xét Nghiệm"
        verbose_name_plural = "Kết Quả Xét Nghiệm"

class DanhMucChuongBenh(models.Model):
    stt = models.CharField(max_length=5, null=True, blank=True)
    ma_chuong = models.CharField(max_length=15, null=True, blank=True)
    ten_chuong = models.CharField(max_length=255, null=True, blank=True)

    objects = BulkUpdateOrCreateQuerySet.as_manager()

    class Meta:
        verbose_name = "Danh Mục Chương Bệnh"
        verbose_name_plural = "Danh Mục Chương Bệnh" 

    def __str__(self):
        return self.stt + f" ({self.ma_chuong})"

class DanhMucNhomBenh(models.Model):
    chuong_benh = models.ForeignKey(DanhMucChuongBenh, on_delete=models.CASCADE, null=True, blank=True, related_name="nhom_benh")
    ma_nhom_chinh = models.CharField(max_length=15, null=True, blank=True)
    ten_nhom_chinh = models.CharField(max_length=255, null=True, blank=True)
    ma_nhom_phu_1 = models.CharField(max_length=15, null=True, blank=True)
    ten_nhom_phu_1 = models.CharField(max_length=255, null=True, blank=True)
    ma_nhom_phu_2 = models.CharField(max_length=15, null=True, blank=True)
    ten_nhom_phu_2 = models.CharField(max_length=255, null=True, blank=True)

    objects = BulkUpdateOrCreateQuerySet.as_manager()

    class Meta:
        verbose_name = "Danh Mục Nhóm Bệnh"
        verbose_name_plural = "Danh Mục Nhóm Bệnh"

    def __str__(self):
        return self.ten_nhom_chinh

class DanhMucLoaiBenh(models.Model):
    nhom_benh = models.ForeignKey(DanhMucNhomBenh, on_delete=models.CASCADE, null=True, blank=True, related_name="loai_benh")
    ma_loai = models.CharField(max_length=10, null=True, blank=True)
    ten_loai = models.CharField(max_length=255, null=True, blank=True)

    objects = BulkUpdateOrCreateQuerySet.as_manager()

    class Meta:
        verbose_name = "Danh Mục Loại Bệnh"
        verbose_name_plural = "Danh Mục Loại Bệnh"
    
    def __str__(self):
        return self.ten_loai

class DanhMucBenh(models.Model):
    loai_benh = models.ForeignKey(DanhMucLoaiBenh, on_delete=models.CASCADE, null=True, blank=True, related_name="benh")
    ma_benh = models.CharField(max_length=15, null=True, blank=True)
    ten_benh = models.CharField(max_length=1024, null=True, blank=True)
    ma_nhom_bcao_byt = models.CharField(max_length=5, null=True, blank=True)
    ma_nhom_chi_tiet = models.CharField(max_length=10, null=True, blank=True)

    objects = BulkUpdateOrCreateQuerySet.as_manager()

    class Meta:
        verbose_name = "Danh Mục Bệnh"
        verbose_name_plural = "Danh Mục Bệnh"

    def __str__(self):
        return self.ten_benh

class NhomChiPhi(models.Model):
    ma_nhom = models.CharField(max_length=2, null=True, blank=True)
    ten_nhom = models.CharField(max_length=255, null=True, blank=True)
    ghi_chu = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Nhóm Chi Phí"
        verbose_name_plural = "Nhóm Chi Phí"

    def __str__(self):
        return f"({self.ma_nhom}) {self.ten_nhom}"

class NhomTaiNan(models.Model):
    ma_nhom = models.CharField(max_length=2, null=True, blank=True)
    ten_nhom = models.CharField(max_length=100, null=True, blank=True)
    ghi_chu = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Nhóm Tai Nạn"
        verbose_name_plural = "Nhóm Tai Nạn"

class DanhMucKhoa(models.Model):
    stt = models.IntegerField(null=True, blank=True)
    ma_khoa = models.CharField(max_length=5, null=True, blank=True)
    ten_khoa = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Danh Mục Khoa"
        verbose_name_plural = "Danh Mục Khoa"

class ThietBi(models.Model):
    ma_may = models.CharField(max_length=50, null=True, blank=True)
    ten_may = models.CharField(max_length=255, null=True, blank=True)
    ghi_chu = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Thiết Bị"
        verbose_name_plural = "Thiết Bị"

class GoiThau(models.Model):
    ma_goi = models.CharField(max_length=5, null=True, blank=True)
    goi = models.CharField(max_length=255, null=True, blank=True)
    nhom = models.CharField(max_length=255, null=True, blank=True)
    ma_nhom = models.CharField(max_length=5, null=True, blank=True)

    class Meta:
        verbose_name = "Gói Thầu"
        verbose_name_plural = "Gói Thầu"

class DuongDungThuoc(models.Model):
    stt = models.IntegerField(null=True, blank=True)
    ma_duong_dung = models.CharField(max_length=5, null=True, blank=True)
    ten_duong_dung = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Đường Dùng Thuốc"
        verbose_name_plural = "Đường Dùng Thuốc"

class MauPhieu(models.Model):
    dich_vu = models.ForeignKey(DichVuKham, on_delete=models.SET_NULL, null=True, blank=True, related_name="mau_phieu")
    ten_mau = models.CharField(max_length=255, null=True, blank=True)
    noi_dung = models.TextField()

    thoi_gian_tao = models.DateTimeField(editable=False, null=True, blank=True)
    thoi_gian_cap_nhat = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Mẫu Phiếu"
        verbose_name_plural = "Mẫu Phiếu"

    def save(self, *args, **kwargs):
        if not self.id:
            self.thoi_gian_tao = timezone.now()
        self.thoi_gian_cap_nhat = timezone.now()
        return super(MauPhieu, self).save(*args, **kwargs)