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

# CSS tùy chỉnh để giao diện sắc nét và ấn tượng hơn
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        .sidebar .sidebar-content { background-color: #1e1e2f; color: white; }
        h1, h2, h3 { color: #1f2937; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .stMetric { background-color: #ffffff; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
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

# --- THANH MENU BÊN TRÁI (SIDEBAR PHONG CÁCH EXECUTIVE) ---
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

# --- NỘI DUNG HIỂN THỊ THEO MODULE ---

if menu == "1. Tổng Quan Điều Hành (Executive Overview)":
    st.title("⚡ Tổng Quan Điều Hành (Executive Overview)")
    st.markdown("Hệ thống quản lý và thống kê dữ liệu học tập thông minh.")
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
    st.title("📁 Cơ Sở Dữ Liệu & Bộ Lọc Nâng Cao")
    st.markdown("Bảng dữ liệu chi tiết toàn bộ học phần của 10 sinh viên.")
    st.markdown("---")
    st.dataframe(df, use_container_width=True)

elif menu == "3. Tra Cứu Hồ Sơ & Đánh Giá Cá Nhân":
    st.title("🔍 Tra Cứu Hồ Sơ & Đánh Giá Cá Nhân")
    st.markdown("Truy xuất nhanh thông tin chi tiết và xếp loại của từng sinh viên.")
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
    st.title("📈 Biểu Đồ Phân Phối Đa Chiều")
    st.markdown("Trực quan hóa trực quan bảng điểm tổng kết của toàn bộ sinh viên.")
    st.markdown("---")
    
    fig, ax = plt.subplots(figsize=(10, 4.5))
    bars = ax.bar(df['Họ và tên'], df['Tong_ket'], color='#3b82f6', edgecolor='#1e3a8a', linewidth=1.2, width=0.6)
    ax.set_ylabel('Điểm Tổng Kết', fontsize=11, fontweight='bold')
    ax.set_xlabel('Họ và Tên Sinh Viên', fontsize=11, fontweight='bold')
    ax.set_ylim(0, 10)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),  
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

    st.pyplot(fig)

# Chân trang (Footer)
st.markdown("---")
st.markdown("<p style='text-align: center; color: #6b7280; font-size: 13px;'>Họ và tên: Phan Khải Trí | MSSV: 066208002686</p>", unsafe_allow_html=True)
