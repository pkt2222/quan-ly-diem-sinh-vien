import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cấu hình giao diện hiện đại
st.set_page_config(
    page_title="Executive Portal - Quản Lý Điểm Sinh Viên",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh màu sắc và phong cách nổi bật, sinh động
st.markdown("""
    <style>
        .main { background-color: #f0f4f8; }
        h1 { color: #0f172a; font-family: 'Segoe UI', sans-serif; }
        .stMetric { background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); padding: 15px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-left: 5px solid #3b82f6; }
    </style>
""", unsafe_allow_html=True)

# Tạo dữ liệu 10 sinh viên đồng bộ
data = {
    'Họ và tên': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Lan', 'Minh', 'Nam', 'Phúc', 'Trang'],
    'Chuyên cần': [8.5, 9.0, 7.0, 9.5, 8.0, 6.5, 9.0, 7.5, 8.0, 9.5],
    'Giữa kỳ': [7.5, 8.0, 6.5, 8.5, 7.0, 6.0, 8.5, 7.0, 7.5, 9.0],
    'Cuối kỳ': [8.0, 8.5, 6.0, 9.0, 7.5, 5.5, 8.5, 6.5, 7.0, 9.0]
}

df = pd.DataFrame(data)

# Chuyển cột STT hiển thị từ 1 đến 10 thay vì 0 đến 9
df.index = range(1, len(df) + 1)
df.index.name = 'STT'

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
st.sidebar.title("🏢 EXECUTIVE PORTAL")
st.sidebar.markdown("---")
st.sidebar.markdown("**Sinh viên:** Phan Khải Trí")
st.sidebar.markdown("**MSSV:** 066208002686")
st.sidebar.markdown("---")

st.sidebar.subheader("📌 HỆ THỐNG MODULE")
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
st.sidebar.success("🟢 Trạng thái hệ thống: Hoạt động ổn định")

# --- NỘI DUNG HIỂN THỊ TỪNG TRANG VỚI MÀU SẮC RIÊNG BIỆT, BẮT MẮT ---

if menu == "1. Tổng Quan Điều Hành (Executive Overview)":
    st.markdown("<h1 style='color: #1e3a8a;'>⚡ Tổng Quan Điều Hành (Executive Overview)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569; font-size: 16px;'>Bảng tổng hợp các chỉ số và dữ liệu thống kê chung của lớp học.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    dtb_lop = df['Tong_ket'].mean()
    sv_max = df.loc[df['Tong_ket'].idxmax()]
    sv_min = df.loc[df['Tong_ket'].idxmin()]
    so_luong_dat = (df['Tong_ket'] >= 5.0).sum()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📈 Điểm trung bình lớp", value=f"{dtb_lop:.2f}")
    with col2:
        st.metric(label="👥 Số sinh viên đạt (>=5.0)", value=so_luong_dat)
    with col3:
        st.metric(label="🏆 Điểm cao nhất", value=f"{sv_max['Tong_ket']}", delta=sv_max['Họ và tên'])
    with col4:
        st.metric(label="⚠️ Điểm thấp nhất", value=f"{sv_min['Tong_ket']}", delta=sv_min['Họ và tên'], delta_color="inverse")

elif menu == "2. Cơ Sở Dữ Liệu & Bộ Lọc Nâng Cao":
    st.markdown("<h1 style='color: #047857;'>📁 Cơ Sở Dữ Liệu & Bộ Lọc Nâng Cao</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #047857; font-size: 16px;'>Danh sách chi tiết bảng điểm toàn bộ 10 sinh viên với thứ tự STT chuẩn từ 1 đến 10.</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.dataframe(df, use_container_width=True)

elif menu == "3. Tra Cứu Hồ Sơ & Đánh Giá Cá Nhân":
    st.markdown("<h1 style='color: #b45309;'>🔍 Tra Cứu Hồ Sơ & Đánh Giá Cá Nhân</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #78350f; font-size: 16px;'>Hệ thống tra cứu thông tin chi tiết, điểm thành phần và xếp loại học lực cá nhân.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    selected_student = st.selectbox("🎯 Chọn tên sinh viên cần tra cứu:", df['Họ và tên'])
    student_info = df[df['Họ và tên'] == selected_student].iloc[0]
    
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**Họ và tên:** {student_info['Họ và tên']}")
        st.write(f"- 📝 Điểm Chuyên cần: **{student_info['Chuyên cần']}**")
        st.write(f"- 📖 Điểm Giữa kỳ: **{student_info['Giữa kỳ']}**")
        st.write(f"- 📚 Điểm Cuối kỳ: **{student_info['Cuối kỳ']}**")
    with c2:
        st.success(f"- 📊 **Điểm tổng kết:** {student_info['Tong_ket']}")
        st.warning(f"- 🎓 **Xếp loại học lực:** {student_info['Xep_loai']}")

elif menu == "4. Biểu Đồ Phân Phối Đa Chiều":
    st.markdown("<h1 style='color: #7c3aed;'>📈 Biểu Đồ Phân Phối Đa Chiều</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #5b21b6; font-size: 16px;'>Trực quan hóa biểu đồ cột điểm tổng kết của toàn bộ sinh viên.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    fig, ax = plt.subplots(figsize=(10, 4.5))
    bars = ax.bar(df['Họ và tên'], df['Tong_ket'], color='#8b5cf6', edgecolor='#4c1d95', linewidth=1.2, width=0.6)
    ax.set_ylabel('Điểm Tổng Kết', fontsize=11, fontweight='bold', color='#4c1d95')
    ax.set_xlabel('Họ và Tên Sinh Viên', fontsize=11, fontweight='bold', color='#4c1d95')
    ax.set_ylim(0, 10)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),  
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color='#4c1d95')

    st.pyplot(fig)

# Chân trang (Footer)
st.markdown("---")
st.markdown("<p style='text-align: center; color: #6b7280; font-size: 13px;'>Họ và tên: Phan Khải Trí | MSSV: 066208002686</p>", unsafe_allow_html=True)
