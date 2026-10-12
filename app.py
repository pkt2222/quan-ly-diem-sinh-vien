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
      f"**Học viên:** {DEVELOPER_NAME}<br>**MSSV:** `{STUDENT_ID}`",
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
# TẠO DỮ LIỆU ĐỘC QUYỀN CHO 12 SINH VIÊN
# ==========================================
np.random.seed(888)
data = {
    "Mã Định Danh": [f"STV-2026-{101+i}" for i in range(12)],
    "Họ và Tên": [
        "Phan Khải Trí",
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
        "Lương Thảo Vy",
    ],
    "Chuyên Cần": np.random.randint(8, 10, 12).astype(float),
    "Kiểm Tra Giữa Kỳ": np.round(np.random.uniform(6.5, 9.8, 12), 1),
    "Thi Cuối Kỳ": np.round(np.random.uniform(5.5, 10.0, 12), 1),
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
            <p>Phát triển và vận hành bởi kỹ sư: <b>{DEVELOPER_NAME}</b> | Mã số sinh viên: <b>{STUDENT_ID}</b></p>
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
  else:
    st.dataframe(df, use_container_width=True)

elif menu == "🔍 Tra Cứu Hồ Sơ & Đánh Giá Cá Nhân":
  st.title("🔍 HỒ SƠ ĐÁNH GIÁ NĂNG LỰC CHI TIẾT")
  st.markdown("Tra cứu chuyên sâu bảng điểm từng học viên trong hệ thống.")

  selected_name = st.selectbox("👉 Lựa chọn học viên cần đánh giá:", df["Họ và Tên"])
  student_rec = df[df["Họ và Tên"] == selected_name].iloc[0]

  st.markdown(f"### 📋 Thông tin chi tiết: `{selected_name}`")
  m1, m2, m3, m4 = st.columns(4)
  m1.metric("📘 Chuyên Cần", student_rec["Chuyên Cần"])
  m2.metric("✍️ Giữa Kỳ", student_rec["Kiểm Tra Giữa Kỳ"])
  m3.metric("📝 Cuối Kỳ", student_rec["Thi Cuối Kỳ"])
  m4.metric("📊 Tổng Kết", student_rec["Điểm Tổng Kết"])

  st.markdown("---")
  st.markdown(
      f"### 🏅 Đánh giá xếp loại chuẩn: **{student_rec['Xếp Loại']}**"
  )

  if student_rec["Điểm Tổng Kết"] >= 8.5:
    st.balloons()
    st.success("🌟 Đạt danh hiệu học lực xuất sắc tiêu biểu trong khóa học!")
  elif student_rec["Điểm Tổng Kết"] >= 5.0:
    st.info("✅ Hoàn thành tốt yêu cầu chuẩn đầu ra học phần.")
  else:
    st.error("⚠️ Cần kế hoạch cải thiện và bổ sung kiến thức chuyên môn.")

elif menu == "📈 Biểu Đồ Phân Phối Đa Chiều":
  st.title("📈 PHÂN TÍCH TRỰC QUAN ĐA CHIỀU")
  st.markdown("Biểu đồ so sánh chi tiết mức điểm tổng kết toàn bộ thành viên.")

  fig, ax = plt.subplots(figsize=(10, 5))
  bars = ax.bar(
      df["Họ và Tên"],
      df["Điểm Tổng Kết"],
      color="#4f46e5",
      edgecolor="#3b82f6",
      linewidth=1.5,
  )
  ax.set_ylabel("Điểm Tổng Kết", fontweight="bold")
  ax.set_title("Biểu đồ phân phối điểm tổng kết học viên", fontsize=14, fontweight="bold")
  plt.xticks(rotation=35, ha="right")
  ax.grid(axis="y", linestyle="--", alpha=0.5)

  for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f"{height}",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 4),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontweight="bold",
    )

  st.pyplot(fig)

# ==========================================
# CHÂN TRANG (FOOTER) - KHẲNG ĐỊNH BẢN QUYỀN
# ==========================================
st.markdown("---")
st.markdown(
    f"""
    <p style='text-align: center; color: #64748b; font-size: 14px;'>
        <b>Họ và tên tác giả:</b> {DEVELOPER_NAME} &nbsp;|&nbsp; 
        <b>Mã số sinh viên (MSSV):</b> {STUDENT_ID}<br>
        🛡️ <i>Executive Student Management System | Academic Enterprise Edition</i> 🛡️
    </p>
""",
    unsafe_allow_html=True,
)
