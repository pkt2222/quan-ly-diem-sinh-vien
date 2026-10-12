import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ==========================================
# CẤU HÌNH THÔNG TIN CÁ NHÂN (TÙY CHỈNH TẠI ĐÂY)
# ==========================================
DEVELOPER_NAME = "Phan Khải Trí"
STUDENT_ID = "066208002686"

# Cấu hình giao diện trang web
st.set_page_config(
    page_title=f"Executive Student Hub - {DEVELOPER_NAME}",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS tinh chỉnh giao diện sáng sủa, cực kỳ dễ nhìn
st.markdown(
    """
    <style>
    .main { background-color: #f8fafc; color: #1e293b; }
    /* Tùy chỉnh sidebar sáng sủa, chữ rõ nét */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] * {
        color: #1e293b !important;
    }
    .executive-header {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        padding: 25px 30px;
        border-radius: 16px;
        color: white;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.2);
        margin-bottom: 25px;
    }
    .executive-header h2, .executive-header p {
        color: white !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# SIDEBAR ĐIỀU HƯỚNG CHUYÊN NGHIỆP
# ==========================================
with st.sidebar:
  st.markdown("### 🏢 **EXECUTIVE PORTAL**")
  st.markdown(
      f"**Sinh viên:** {DEVELOPER_NAME}<br><b>MSSV:</b> {STUDENT_ID}",
      unsafe_allow_html=True,
  )
  st.markdown("---")

  menu = st.radio(
      "📍 HỆ THỐNG MODULE",
      [
          "⚡ Tổng Quan Điều Hành (Executive Overview)",
          "📊 Cơ Sở Dữ Liệu & Bộ Lọc Nâng Cao",
          "🔍 Tra Cứu Hồ Sơ & Đánh Giá Cá Nhân",
          "📈 Biểu Đồ Phân Phối Đa Chiều",
      ],
  )
  st.markdown("---")
  st.success("🟢 Trạng thái hệ thống: Hoạt động ổn định")

# ==========================================
# TẠO DỮ LIỆU ĐỘC QUYỀN CHO ĐÚNG 10 HỌC SINH
# ==========================================
np.random.seed(999)
data = {
    "Mã Định Danh": [f"STV-2026-{201+i}" for i in range(10)],
    "Họ và Tên": [
        "Nguyễn Hoàng Long",
        "Trần Minh Thư",
        "Lê Gia Hân",
        "Phạm Bảo Quốc",
        "Vũ Khánh Huyền",
        "Đỗ Minh Quang",
        "Bùi Phương Linh",
        "Ngô Thanh Trúc",
        "Dương Gia Huy",
        "Hồ Hải Nam",
    ],
    "Chuyên Cần": np.random.randint(8, 10, 10).astype(float),
    "Kiểm Tra Giữa Kỳ": np.round(np.random.uniform(6.5, 9.8, 10), 1),
    "Thi Cuối Kỳ": np.round(np.random.uniform(5.5, 10.0, 10), 1),
}

df = pd.DataFrame(data)

# Thuật toán tính điểm trọng số tinh chỉnh (10% - 30% - 60%)
df["Điểm Tổng Kết"] = np.round(
    df["Chuyên Cần"] * 0.1
    + df["Kiểm Tra Giữa Kỳ"] * 0.3
    + df["Thi Cuối Kỳ"] * 0.6,
    2,
)


def xep_loai_chuyen_gia(diem):
  if diem >= 8.5:
    return "🌟 Xuất Sắc (Honor)"
  elif diem >= 7.5:
    return "💎 Giỏi (Distinction)"
  elif diem >= 6.0:
    return "📘 Khá (Merit)"
  elif diem >= 5.0:
    return "🟢 Đạt (Standard)"
  else:
    return "⚠️ Cần Cải Thiện"


df["Xếp Loại"] = df["Điểm Tổng Kết"].apply(xep_loai_chuyen_gia)

# ==========================================
# GIAO DIỆN CÁC MODULE CHỨC NĂNG
# ==========================================

if menu == "⚡ Tổng Quan Điều Hành (Executive Overview)":
  st.markdown(
      f"""
        <div class="executive-header">
            <h2>🛡️ HỆ THỐNG QUẢN LÝ VÀ PHÂN TÍCH ĐIỂM SỐ EXECUTIVE</h2>
            <p>Phát triển và vận hành bởi sinh viên: <b>{DEVELOPER_NAME}</b> | Mã số sinh viên: <b>{STUDENT_ID}</b></p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  dtb_chung = np.round(df["Điểm Tổng Kết"].mean(), 2)
  sv_xuat_sac = len(df[df["Điểm Tổng Kết"] >= 8.5])
  sv_dat = len(df[df["Điểm Tổng Kết"] >= 5.0])
  top_student = df.loc[df["Điểm Tổng Kết"].idxmax()]

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(
        label="👥 Tổng Sĩ Số Quản Lý",
        value=f"{len(df)} Học Viên",
        delta="Dữ liệu chuẩn",
    )
  with col2:
    st.metric(
        label="📊 Điểm Trung Bình Khối",
        value=f"{dtb_chung} / 10",
        delta="Hiệu suất tối ưu",
    )
  with col3:
    st.metric(
        label="🌟 Số Lượng Đạt Loại Giỏi+",
        value=f"{sv_xuat_sac} Học Viên",
        delta=f"{(sv_xuat_sac/len(df))*100:.1f}%",
    )
  with col4:
    st.metric(
        label="🏆 Thủ Khoa Dẫn Đầu",
        value=f"{top_student['Điểm Tổng Kết']}đ",
        delta=top_student["Họ và Tên"],
    )

  st.markdown("---")

  c_left, c_right = st.columns([1.3, 1])

  with c_left:
    st.subheader("📈 Phân Phối Điểm Tổng Kết Toàn Khóa")
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(
        df["Họ và Tên"],
        df["Điểm Tổng Kết"],
        marker="s",
        color="#4f46e5",
        linewidth=2.5,
        markersize=7,
    )
    ax.fill_between(df["Họ và Tên"], df["Điểm Tổng Kết"], color="#3b82f6", alpha=0.1)
    ax.set_ylabel("Điểm Tổng Kết")
    plt.xticks(rotation=35, ha="right")
    ax.grid(True, linestyle="--", alpha=0.3)
    st.pyplot(fig)

  with c_right:
    st.subheader("📌 Báo Cáo Nhận Định Hệ Thống")
    st.info(
        f"🥇 **Học viên xuất sắc nhất:** `{top_student['Họ và Tên']}` ("
        f"{top_student['Mã Định Danh']}) đạt thành tích cao nhất với"
        f" **{top_student['Điểm Tổng Kết']}** điểm."
    )
    st.success(
        "💡 **Đánh giá năng lực:** Tỷ lệ học viên đạt tiêu chuẩn chuyên môn"
        f" đạt **{(sv_dat/len(df))*100:.0f}%**, phân bổ điểm số minh bạch và"
        " đồng đều theo ma trận đánh giá."
    )
    st.warning(
        "⚙️ **Bảo mật dữ liệu:** Hệ thống được mã hóa định danh theo tiêu chuẩn"
        f" học tập của sinh viên **{DEVELOPER_NAME}**."
    )

elif menu == "📊 Cơ Sở Dữ Liệu & Bộ Lọc Nâng Cao":
  st.title("📊 TRUNG TÂM CƠ SỞ DỮ LIỆU ĐIỂM SỐ")
  st.markdown(
      "Truy xuất, lọc dữ liệu và xuất báo cáo tự động theo chuẩn doanh nghiệp."
  )

  c_f1, c_f2 = st.columns([2, 1])
  with c_f1:
    search_key = st.text_input(
        "🔍 Tra cứu nhanh theo Mã định danh hoặc Họ tên:", ""
    )
  with c_f2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        label="📥 Trích xuất báo cáo (.CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=f"bao_cao_diem_{STUDENT_ID}.csv",
        mime="text/csv",
    )

  if search_key:
    filtered_df = df[
        df["Họ và Tên"].str.contains(search_key, case=False, na=False)
        | df["Mã Định Danh"].str.contains(search_key, case=False, na=False)
    ]
    st.dataframe(filtered_df, use_container_width=True)
