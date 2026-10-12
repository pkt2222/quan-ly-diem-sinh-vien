import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Hệ Thống Quản Lý Điểm Sinh Viên", page_icon="🎓", layout="wide"
)

# Tùy chỉnh giao diện CSS hiện đại
st.markdown(
    """
    <style>
    .main { background-color: #f1f5f9; }
    .stMetric {
        background: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar điều hướng
with st.sidebar:
  st.title("🎓 Quản Lý Học Tập")
  st.markdown("Hệ thống quản lý điểm số thế hệ mới.")
  st.markdown("---")
  menu = st.radio(
      "📍 Chọn chức năng:",
      [
          "📊 Tổng Quan Dashboard",
          "📋 Bảng Điểm Chi Tiết",
          "🔍 Tra Cứu Cá Nhân",
          "📈 Biểu Đồ Phân Tích",
      ],
  )
  st.markdown("---")
  st.info("💡 Mẹo: Sử dụng menu bên trên để chuyển tab nhanh chóng.")

# Khởi tạo dữ liệu mẫu 10 sinh viên
np.random.seed(42)
data = {
    "Mã SV": [f"SV{2026101+i}" for i in range(10)],
    "Họ tên": [
        "Nguyễn Văn An",
        "Trần Thị Bình",
        "Lê Hoàng Cường",
        "Phạm Thị Dung",
        "Hoàng Văn Em",
        "Vũ Thị Phương",
        "Đỗ Minh Giang",
        "Bùi Thị Hoa",
        "Ngô Văn Hùng",
        "Dương Thị Kim",
    ],
    "Chuyên cần": np.random.randint(8, 10, 10).astype(float),
    "Giữa kỳ": np.round(np.random.uniform(6.0, 9.5, 10), 1),
    "Cuối kỳ": np.round(np.random.uniform(5.5, 10.0, 10), 1),
}

df = pd.DataFrame(data)
df["Tổng kết"] = np.round(
    df["Chuyên cần"] * 0.1 + df["Giữa kỳ"] * 0.3 + df["Cuối kỳ"] * 0.6, 1
)


def xep_loai(diem):
  if diem >= 8.5:
    return "🌟 Xuất Sắc"
  elif diem >= 7.0:
    return "🎯 Giỏi / Khá"
  elif diem >= 5.0:
    return "📘 Đạt"
  else:
    return "⚠️ Cần cố gắng"


df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# Xhiển thị nội dung theo Menu Sidebar
if menu == "📊 Tổng Quan Dashboard":
  st.title("📊 Tổng Quan Hệ Thống Quản Lý")
  st.markdown(
      "Chào mừng bạn đến với bảng điều khiển phân tích học tập toàn diện của lớp"
      " học."
  )
  st.markdown("---")

  dtb_lop = np.round(df["Tổng kết"].mean(), 2)
  so_sv_dat = len(df[df["Tổng kết"] >= 5.0])
  max_sv = df.loc[df["Tổng kết"].idxmax()]
  min_sv = df.loc[df["Tổng kết"].idxmin()]

  col1, col2, col3, col4 = st.columns(4)
  col1.metric("👥 Tổng Sĩ Số", f"{len(df)} SV")
  col2.metric("⭐ Điểm Trung Bình Lớp", f"{dtb_lop} / 10")
  col3.metric("✅ Tỷ Lệ Đạt", f"{(so_sv_dat/len(df))*100}%")
  col4.metric("🏆 Điểm Cao Nhất", f"{max_sv['Tổng kết']}")

  st.markdown("---")
  c1, c2 = st.columns(2)
  with c1:
    st.success(
        f"🥇 **Vị trí Thủ khoa:** {max_sv['Họ tên']} với số điểm tổng kết"
        f" **{max_sv['Tổng kết']}**."
    )
  with c2:
    st.warning(
        f"⚠️ **Cần quan tâm:** {min_sv['Họ tên']} với số điểm tổng kết"
        f" **{min_sv['Tổng kết']}**."
    )

elif menu == "📋 Bảng Điểm Chi Tiết":
  st.title("📋 Bảng Điểm Toàn Khóa")
  keyword = st.text_input("🔍 Tìm kiếm sinh viên (nhập tên hoặc mã SV):", "")
  if keyword:
    filtered = df[
        df["Họ tên"].str.contains(keyword, case=False, na=False)
        | df["Mã SV"].str.contains(keyword, case=False, na=False)
    ]
    st.dataframe(filtered, use_container_width=True)
  else:
    st.dataframe(df, use_container_width=True)

  st.download_button(
      label="📥 Tải xuống danh sách điểm (.csv)",
      data=df.to_csv(index=False).encode("utf-8"),
      file_name="bang_diem_lop.csv",
      mime="text/csv",
  )

elif menu == "🔍 Tra Cứu Cá Nhân":
  st.title("🔍 Tra Cứu Hồ Sơ Học Tập")
  selected_student = st.selectbox("👉 Lựa chọn tên sinh viên:", df["Họ tên"])
  s_info = df[df["Họ tên"] == selected_student].iloc[0]

  st.markdown(f"### Thông tin chi tiết của: `{selected_student}`")
  m1, m2, m3, m4 = st.columns(4)
  m1.metric("📘 Chuyên cần", s_info["Chuyên cần"])
  m2.metric("✍️ Giữa kỳ", s_info["Giữa kỳ"])
  m3.metric("📝 Cuối kỳ", s_info["Cuối kỳ"])
  m4.metric("📊 Tổng kết", s_info["Tổng kết"])

  st.markdown(f"### 🏅 Đánh giá học lực: **{s_info['Xếp loại']}**")

elif menu == "📈 Biểu Đồ Phân Tích":
  st.title("📈 Phân Tích Biểu Đồ Trực Quan")
  fig, ax = plt.subplots(figsize=(10, 4.5))
  bars = ax.bar(
      df["Họ tên"],
      df["Tổng kết"],
      color="#3b82f6",
      edgecolor="#1d4ed8",
      linewidth=1.5,
  )
  ax.set_ylabel("Điểm Tổng Kết", fontweight="bold")
  ax.set_title("Biểu đồ cột điểm tổng kết toàn lớp", fontsize=13, fontweight="bold")
  plt.xticks(rotation=30, ha="right")
  ax.grid(axis="y", linestyle="--", alpha=0.5)

  for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f"{height}",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontweight="bold",
    )
  st.pyplot(fig)

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Student Management System |"
    " Professional Edition</p>",
    unsafe_allow_html=True,
)
