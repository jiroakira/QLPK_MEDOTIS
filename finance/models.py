from django.db import models
from django.utils import timezone

class HoaDonThuoc(models.Model):
    # benh_nhan = models.ForeignKey(NguoiDung, on_delete=models.SET(get_sentinel_user))
    """ 
    * Bảng hóa đơn thuốc sẽ lưu trữ lại hóa đơn của tất cả người dùng
    
    @field chuoi_kham: mối quan hệ 1-1 với Chuỗi Khám, vì một chuỗi khám sẽ chỉ có một hóa đơn
    @field ma_hoa_don: mã hóa đơn này sẽ do bác sĩ tự quy định, bác sĩ có thể quy định mã hóa đơn này theo người bệnh và thời gian họ khám để dễ dàng phân biệt
    @field tong_tien: tổng số tiền của các thuốc mà bệnh nhân đã được kê đơn
    @field thoi_gian_tao: thời gian hóa đơn được tạo
    @field thoi_gian_cap_nhat: thời gian hóa đơn được cập nhật
    """
    don_thuoc = models.OneToOneField("medicine.DonThuoc", on_delete=models.SET_NULL, null=True, related_name='hoa_don_thuoc')
    ma_hoa_don = models.CharField(max_length=255, unique=True, null=True, blank=True)
    tong_tien = models.DecimalField(decimal_places=0, max_digits=10, null=True, blank=True)
    thoi_gian_tao = models.DateTimeField(editable=False, null=True, blank=True)
    thoi_gian_cap_nhat = models.DateTimeField(null=True, blank=True)
    bao_hiem = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.thoi_gian_tao = timezone.now()
        self.thoi_gian_cap_nhat = timezone.now()
        return super(HoaDonThuoc, self).save(*args, **kwargs)

class HoaDonChuoiKham(models.Model):
    """ 
    * Bảng hóa đơn khám sẽ lưu trữ lại hóa đơn sau khi sử dụng các dịch vụ khám của tất cả người dùng 

    @field chuoi_kham: mối quan hệ 1-1 với Chuỗi Khám, vì một chuỗi khám sẽ chỉ có một hóa đơn
    @field ma_hoa_don: mã hóa đơn này sẽ do bác sĩ tự quy định, bác sĩ có thể quy định mã hóa đơn này theo người bệnh và thời gian họ khám để dễ dàng phân biệt
    @field tong_tien: tổng số tiền của các dịch vụ khám mà bệnh nhân đã khám
    @field thoi_gian_tao: thời gian hóa đơn được tạo
    @field thoi_gian_cap_nhat : thời gian hóa đơn được cập nhật
    """

    chuoi_kham = models.OneToOneField("clinic.ChuoiKham", on_delete=models.SET_NULL, null=True, related_name='hoa_don_dich_vu')
    ma_hoa_don = models.CharField(max_length=255, null=True, blank=True, unique=True)
    tong_tien = models.DecimalField(decimal_places=3, max_digits=10, null=True, blank=True)
    thoi_gian_tao = models.DateTimeField(editable=False, null=True, blank=True)
    thoi_gian_cap_nhat = models.DateTimeField(null=True, blank=True)

    bao_hiem = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.thoi_gian_tao = timezone.now()
        self.thoi_gian_cap_nhat = timezone.now()
        return super(HoaDonChuoiKham, self).save(*args, **kwargs)

    def get_ma_benh(self):
        try:
            return self.chuoi_kham.ket_qua_tong_quat.all()[0].ma_benh.ma_benh
        except:
            return ''

    def get_tong_cong(self):
        ds_dich_vu = self.chuoi_kham.phan_khoa_kham.all()
        tong_tien = []
        for phan_khoa in ds_dich_vu:
            gia = phan_khoa.dich_vu_kham.don_gia
            tong_tien.append(gia)
        return sum(tong_tien)

    def get_tong_cong_2(self):
        tong_cong_2 = float(self.get_tong_cong()) - float(self.tong_tien)
        return tong_cong_2

    # TODO: trường tổng tiền có trong 2 hóa đơn sẽ được update sau khi bệnh nhân đóng tiền (transaction atomic update)

class HoaDonLamSang(models.Model):
    lich_hen = models.ForeignKey("clinic.LichHenKham", on_delete=models.SET_NULL, null=True, blank=True, related_name="hoa_don_lam_sang")
    tong_tien = models.DecimalField(max_digits=20, decimal_places=3, null=True, blank=True)
    thoi_gian_tao = models.DateTimeField(editable=False, null=True, blank=True)
    thoi_gian_cap_nhat = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.thoi_gian_tao = timezone.now()
        self.thoi_gian_cap_nhat = timezone.now()
        return super(HoaDonLamSang, self).save(*args, **kwargs)

    # benh_nhan = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)

class HoaDonTong(models.Model):
    benh_nhan = models.ForeignKey("clinic.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="hoa_don_tong_nguoi_dung")
    lich_hen = models.ForeignKey("clinic.LichHenKham", on_delete=models.SET_NULL, null=True, blank=True, related_name="hoa_don_lich_hen")
    hoa_don_lam_sang = models.ForeignKey(HoaDonLamSang, on_delete=models.SET_NULL, null=True, blank=True)
    hoa_don_chuoi_kham = models.ForeignKey(HoaDonChuoiKham, on_delete=models.SET_NULL, null=True, blank=True)
    hoa_don_thuoc = models.ForeignKey(HoaDonThuoc, on_delete=models.SET_NULL, null=True, blank=True)
    bao_hiem = models.BooleanField(default=False)

    thoi_gian_tao = models.DateTimeField(editable=False, null=True, blank=True)
    thoi_gian_cap_nhat = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.thoi_gian_tao = timezone.now()
        self.thoi_gian_cap_nhat = timezone.now()
        return super(HoaDonTong, self).save(*args, **kwargs)

# NEW FROM LONG
class HoaDonVatTu(models.Model):
    nguoi_phu_trach = models.ForeignKey("clinic.User", on_delete=models.SET_NULL, null=True, blank=True)
    tong_tien = models.DecimalField(max_digits=20, decimal_places=3, null=True, blank=True)
    bao_hiem = models.BooleanField(default=False)

    thoi_gian_tao = models.DateTimeField(editable=False, null=True, blank=True)
    thoi_gian_cap_nhat = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.thoi_gian_tao = timezone.now()
        self.thoi_gian_cap_nhat = timezone.now()
        return super(HoaDonVatTu, self).save(*args, **kwargs)
# END