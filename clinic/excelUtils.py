from io import BytesIO 
import xlsxwriter
from django.utils.translation import ugettext

def WriteToExcel(excel_data):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    workbook.encoding='utf-8'
    worksheet_s = workbook.add_worksheet("Summary")

    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    cell = workbook.add_format({
        'align': 'left',
        'valign': 'top',
        'text_wrap': True,
        'border': 1
    })
    cell_center = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'border': 1
    })

    worksheet_s.merge_range('A1:D1', "Phòng Khám Đa Khoa MEDOTIS", cell_center)
    worksheet_s.merge_range('S1:W1', "Mẫu số: C79a-HD", cell_center)
    worksheet_s.merge_range('S2:W3', "Ban hành theo thông tư số 178/2012/TT-BTC ngày 23/10/2012 của Bộ Tài chính)", cell_center)

    worksheet_s.merge_range('A4:W4', "DANH SÁCH NGƯỜI BỆNH BẢO HIỂM Y TẾ KHÁM CHỮA BỆNH NGOẠI TRÚ ĐỀ NGHỊ THANH TOÁN", title)
    # worksheet_s.merge_range('H5:P5', )
    worksheet_s.merge_range('A7:A9', "STT", cell_center)
    worksheet_s.merge_range('B7:B9', "Họ và tên", cell_center)
    worksheet_s.merge_range('C7:D8', "Năm sinh", cell_center)
    worksheet_s.write(8, 2, 'Nam', cell_center)
    worksheet_s.write(8, 3, 'Nữ', cell_center)
    worksheet_s.merge_range('E7:E9', "Mã thẻ BHYT", cell_center)
    worksheet_s.merge_range('F7:F9', "Mã ĐKBĐ", cell_center)
    worksheet_s.merge_range('G7:G9', "Mã bệnh", cell_center)
    worksheet_s.merge_range('I7:T7', "TỔNG CHI PHÍ KHÁM, CHỮA BỆNH BHYT", cell_center)
    worksheet_s.merge_range('I8:I9', "Tổng cộng", cell_center)
    worksheet_s.merge_range('J8:O8', "Không áp dụng tỉ lệ thanh toán", cell_center)
    worksheet_s.merge_range('H7:H9', "Ngày khám", cell_center)
    worksheet_s.write(8, 9, 'Xét nghiệm', cell_center)
    worksheet_s.write(8, 10, 'CĐHA TDCN', cell_center)
    worksheet_s.write(8, 11, 'Thuốc', cell_center)

    worksheet_s.set_row(8, 60) 
    
    worksheet_s.write(8, 12, 'Máu', cell_center)
    worksheet_s.write(8, 13, 'TTPT', cell_center)
    worksheet_s.write(8, 14, 'VTYT', cell_center)
    worksheet_s.merge_range('P8:R8', "Thanh toán theo tỷ lệ", cell_center)
    worksheet_s.write(8, 15, 'DVKT', cell_center)
    worksheet_s.write(8, 16, 'Thuốc', cell_center)
    worksheet_s.write(8, 17, 'VTYT', cell_center)
    worksheet_s.merge_range('S8:S9', "Tiền khám", cell_center)
    worksheet_s.merge_range('T8:T9', "Vận chuyển", cell_center)
    worksheet_s.merge_range('U7:U9', "Người bệnh chi trả", cell_center)
    worksheet_s.merge_range('V7:W7', "Chi phí đề nghị BHXH thanh toán", cell_center)
    worksheet_s.write(8, 21, 'Tổng cộng', cell_center)
    worksheet_s.write(8, 22, 'Trong đó chi phí ngoài quỹ định suất', cell_center)

    for idx, data in enumerate(excel_data):
        row = 10 + idx
        worksheet_s.write(row, 1, data['benh_nhan'], cell_center)
        if data['gioi_tinh'] == '1':
            worksheet_s.write(row, 2, data['nam_sinh'], cell_center)
        elif data['gioi_tinh'] == '2':
            worksheet_s.write(row, 3, data['nam_sinh'], cell_center)
        worksheet_s.write(row, 4, data['ma_bhyt'], cell_center)
        worksheet_s.write(row, 5, data['ma_dkbd'], cell_center)
        worksheet_s.write(row, 6, data['ma_benh'], cell_center)

        worksheet_s.write(row, 8, data['tong_cong_1'], cell_center)
        worksheet_s.write(row, 18, data['tien_kham'], cell_center)
        worksheet_s.write(row, 20, data['tu_chi_tra'], cell_center)
        worksheet_s.write(row, 21, data['tong_cong_2'], cell_center)
        

    workbook.close()

    xlsx_data = output.getvalue()
    return xlsx_data

