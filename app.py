import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cấu hình tiêu đề trang
st.set_page_config(page_title="Quản Lý Điểm Sinh Viên", layout="wide")

# Tạo dữ liệu 10 sinh viên đồng bộ
data = {
    'Họ và tên': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Lan', 'Minh', 'Nam', 'Phúc', 'Trang'],
    'Chuyên cần': [8.5, 9.0, 7.0, 9.5, 8.0, 6.5, 9.0, 7.5, 8.0, 9.5],
    'Giữa kỳ': [7.5, 8.0, 6.5, 8.5, 7.0, 6.0, 8.5, 7.0, 7.5, 9.0],
    'Cuối kỳ': [8.0, 8.5, 6.0, 9.0, 7.5, 5.5, 8.5, 6.5, 7.0, 9.0]
}

df = pd.DataFrame(data)

# Tính điểm tổng kết
df['Tong_ket'] = (0.2 * df['Chuyên cần'] + 0.3 * df['Giữa kỳ'] + 0.5 * df['Cuối kỳ']).round(2)

# Xếp loại sinh viên
def xep_loai(diem):
    if diem >= 8.5:
        return 'Giỏi'
    elif diem >= 7.0:
        return 'Khá'
    elif diem >= 5.0:
        return 'Trung bình'
    else:
        return 'Yếu'

df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)

# --- THANH MENU BÊN TRÁI (SIDEBAR) ---
st.sidebar.title("EXECUTIVE PORTAL")
st.sidebar.markdown("---")
# Bổ sung hiển thị thông tin sinh viên rõ ràng tại sidebar
st.sidebar.markdown("### 👤 Thông tin sinh viên")
st.sidebar.write("**Họ và tên:** Phan Khải Trí")
st.sidebar.write("**MSSV:** 066208002686")
st.sidebar.write("**Lớp:** 12B6")
st.sidebar.markdown("---")

st.sidebar.subheader("HỆ THỐNG MODULE")
menu = st.sidebar.radio(
    "Chọn module:",
    [
        "1. Tổng Quan Điều Hành (Executive Overview)",
        "2. Cơ Sở Dữ Liệu & Bộ Lọc Nâng Cao",
        "3. Tra Cứu Hồ Sơ & Đánh Giá Cá Nhân",
        "4. Biểu Đồ Phân Phối Đa Chiều"
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("Trạng thái hệ thống: Hoạt động ổn định")

# --- NỘI DUNG HIỂN THỊ THEO MENU ĐƯỢC CHỌN ---

if menu == "1. Tổng Quan Điều Hành (Executive Overview)":
    st.title("QUẢN LÝ ĐIỂM SINH VIÊN - TỔNG QUAN")
    st.subheader("📊 Thống kê chung của lớp")
    
    dtb_lop = df['Tong_ket'].mean()
    sv_max = df.loc[df['Tong_ket'].idxmax()]
    sv_min = df.loc[df['Tong_ket'].idxmin()]
    so_luong_dat = (df['Tong_ket'] >= 5.0).sum()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Điểm trung bình lớp", value=f"{dtb_lop:.2f}")
        st.metric(label="Số sinh viên đạt (>= 5.0)", value=so_luong_dat)
    with col2:
        st.metric(label="SV điểm cao nhất", value=f"{sv_max['Họ và tên']} ({sv_max['Tong_ket']})")
        st.metric(label="SV điểm thấp nhất", value=f"{sv_min['Họ và tên']} ({sv_min['Tong_ket']})")

elif menu == "2. Cơ Sở Dữ Liệu & Bộ Lọc Nâng Cao":
    st.title("QUẢN LÝ ĐIỂM SINH VIÊN - CƠ SỞ DỮ LIỆU")
    st.subheader("📁 Bảng điểm chi tiết của 10 sinh viên")
    st.dataframe(df, use_container_width=True)

elif menu == "3. Tra Cứu Hồ Sơ & Đánh Giá Cá Nhân":
    st.title("QUẢN LÝ ĐIỂM SINH VIÊN - TRA CỨU")
    st.subheader("🔍 Tra cứu thông tin chi tiết từng sinh viên")
    
    selected_student = st.selectbox("Chọn tên sinh viên:", df['Họ và tên'])
    student_info = df[df['Họ và tên'] == selected_student].iloc[0]
    
    st.write(f"**Họ và tên:** {student_info['Họ và tên']}")
    st.write(f"- Điểm chuyên cần: {student_info['Chuyên cần']}")
    st.write(f"- Điểm giữa kỳ: {student_info['Giữa kỳ']}")
    st.write(f"- Điểm cuối kỳ: {student_info['Cuối kỳ']}")
    st.write(f"- **Điểm tổng kết:** {student_info['Tong_ket']}")
    st.write(f"- **Xếp loại:** {student_info['Xep_loai']}")

elif menu == "4. Biểu Đồ Phân Phối Đa Chiều":
    st.title("QUẢN LÝ ĐIỂM SINH VIÊN - TRỰC QUAN HÓA")
    st.subheader("📈 Biểu đồ điểm tổng kết của lớp")
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(df['Họ và tên'], df['Tong_ket'], color='skyblue', edgecolor='black')
    ax.set_ylabel('Điểm tổng kết')
    ax.set_ylim(0, 10)
    for i, v in enumerate(df['Tong_ket']):
        ax.text(i, v + 0.1, str(v), ha='center', fontsize=9, fontweight='bold')
    
    st.pyplot(fig)

# Chân trang (Footer hiển thị tên và MSSV)
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 13px;'>Họ và tên: Phan Khải Trí | MSSV: 066208002686 | Lớp: 12B6</p>", unsafe_allow_html=True)
