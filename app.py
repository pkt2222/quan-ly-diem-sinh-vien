import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# 1. Cấu hình giao diện tổng thể (Wide layout & Dark/Modern theme feel)
st.set_page_config(
    page_title="Hệ Thống Quản Lý Điểm Sinh Viên - Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS để làm đẹp giao diện (Bo góc, đổi màu card, hiệu ứng bóng mờ hiện đại)
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(79, 70, 229, 0.3);
    }
    .stMetric label {
        color: #9ca3af !important;
        font-weight: 600 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar (Thanh bên hiện đại)
with st.sidebar:
  st.image(
      "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=500&auto=format&fit=crop&q=60",
      use_container_width=True,
  )
  st.title("🎓 StudentHub Pro")
  st.markdown("Hệ thống quản lý học tập thông minh thế hệ mới.")
  st.markdown("---")
  menu = st.radio(
      "📍 Điều hướng nhanh",
      [
          "📊 Tổng Quan Dashboard",
          "📋 Bảng Điểm Chi Tiết",
          "🔍 Tra Cứu Cá Nhân",
          "📈 Phân Tích Biểu Đồ",
      ],
  )
  st.markdown("---")
  st.info("💡 Mẹo: Dùng chế độ Dark Mode của Streamlit để hiển thị đẹp nhất!")

# 2. Tạo dữ liệu mẫu sinh động cho 10 sinh viên
np.random.seed(42)
data = {
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

# Tính điểm Tổng kết
df["Tổng kết"] = np.round(
    df["Chuyên cần"] * 0.1 + df["Giữa kỳ"] * 0.3 + df["Cuối kỳ"] * 0.6, 1
)


# Hàm xếp loại chuẩn học thuật
def xep_loai(diem):
  if diem >= 8.5:
    return "🌟 Giỏi"
  elif diem >= 7.0:
    return "🎯 Khá"
  elif diem >= 5.0:
    return "📘 Trung bình"
  else:
    return "⚠️ Cần cố gắng"


df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# 3. Xử lý hiển thị theo Sidebar Menu
if menu == "📊 Tổng Quan Dashboard":
  st.title("⚡ DASHBOARD THỐNG KÊ TỔNG QUAN")
  st.markdown("Cập nhật toàn diện các chỉ số học tập của lớp học.")

  dtb_lop = np.round(df["Tổng kết"].mean(), 2)
  so_sv_dat = len(df[df["Tổng kết"] >= 5.0])
  max_sv = df.loc[df["Tổng kết"].idxmax()]
  min_sv = df.loc[df["Tổng kết"].idxmin()]

  # Các khối Metric nổi bật
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(
        label="👥 Tổng Sĩ Số", value=f"{len(df)} SV", delta="Ổn định lớp"
    )
  with col2:
    st.metric(
        label="⭐ Điểm Trung Bình Lớp",
        value=f"{dtb_lop} / 10",
        delta="Học lực khá",
    )
  with col3:
    st.metric(
        label="✅ Sinh Viên Đạt (>=5.0)",
        value=f"{so_sv_dat} / 10",
        delta=f"{(so_sv_dat/len(df))*100}%",
    )
  with col4:
    st.metric(
        label="🏆 Điểm Cao Nhất",
        value=f"{max_sv['Tổng kết']}",
        delta=max_sv["Họ tên"],
    )

  st.markdown("---")

  # Thông báo nổi bật vinh danh / cảnh báo
  c_left, c_right = st.columns(2)
  with c_left:
    st.success(
        f"🥇 **Thủ khoa lớp:** {max_sv['Họ tên']} đang dẫn đầu với điểm tổng kết"
        f" ấn tượng: **{max_sv['Tổng kết']}**!"
    )
  with c_right:
    st.warning(
        f"⚠️ **Cần lưu ý hỗ trợ:** {min_sv['Họ tên']} (Điểm tổng kết:"
        f" {min_sv['Tổng kết']})."
    )

  # Biểu đồ thu nhỏ ngay trang chủ
  st.sub_header = st.subheader(
      "📈 Biểu đồ xu hướng điểm tổng kết nhanh của lớp"
  )
  fig, ax = plt.subplots(figsize=(10, 3.5))
  ax.plot(
      df["Họ tên"],
      df["Tổng kết"],
      marker="o",
      color="#38bdf8",
      linewidth=2.5,
      markersize=8,
  )
  ax.fill_between(df["Họ tên"], df["Tổng kết"], color="#38bdf8", alpha=0.1)
  ax.set_ylabel("Điểm tổng kết", color="white")
  plt.xticks(rotation=30, ha="right")
  ax.grid(True, linestyle=":", alpha=0.3)
  st.pyplot(fig)

elif menu == "📋 Bảng Điểm Chi Tiết":
  st.title("📋 BẢNG ĐIỂM CHI TIẾT TOÀN LỚP")
  st.markdown("Dữ liệu điểm thành phần và kết quả tổng kết của 10 sinh viên.")

  # Thanh tìm kiếm nhanh trên bảng
  search_query = st.text_input(
      "🔍 Tìm kiếm nhanh sinh viên theo tên:", ""
  )
  if search_query:
    filtered_df = df[
        df["Họ tên"].str.contains(search_query, case=False, na=False)
    ]
    st.dataframe(filtered_df, use_container_width=True)
  else:
    st.dataframe(df, use_container_width=True)

elif menu == "🔍 Tra Cứu Cá Nhân":
  st.title("🔍 TRA CỨU KẾT QUẢ HỌC TẬP CÁ NHÂN")
  st.markdown("Chọn tên sinh viên để xem chi tiết từng cột điểm.")

  selected_student = st.selectbox("👉 Lựa chọn sinh viên:", df["Họ tên"])
  student_info = df[df["Họ tên"] == selected_student].iloc[0]

  # Khung hiển thị thông tin dạng thẻ hiện đại
  st.markdown(f"### Hồ sơ học tập: `{selected_student}`")
  col_a, col_b, col_c, col_d, col_e = st.columns(5)
  col_a.metric("📘 Chuyên cần", student_info["Chuyên cần"])
  col_b.metric("✍️ Giữa kỳ", student_info["Giữa kỳ"])
  col_c.metric("📝 Cuối kỳ", student_info["Cuối kỳ"])
  col_d.metric("📊 Tổng kết", student_info["Tổng kết"])
  col_e.metric("🏅 Xếp loại", student_info["Xếp loại"])

  st.balloons() if student_info["Tổng kết"] >= 8.0 else None

elif menu == "📈 Phân Tích Biểu Đồ":
  st.title("📈 PHÂN TÍCH TRỰC QUAN ĐIỂM SỐ")
  st.markdown("Biểu đồ cột chi tiết điểm số của từng cá nhân trong lớp học.")

  fig, ax = plt.subplots(figsize=(10, 5))
  bars = ax.bar(
      df["Họ tên"],
      df["Tổng kết"],
      color="#6366f1",
      edgecolor="#818cf8",
      linewidth=1.5,
  )
  ax.set_ylabel("Điểm Tổng Kết", fontweight="bold", color="gray")
  ax.set_title("Biểu đồ phân phối điểm Tổng kết", fontsize=14, fontweight="bold")
  plt.xticks(rotation=35, ha="right")
  ax.grid(axis="y", linestyle="--", alpha=0.4)

  # Gắn nhãn số liệu trên đầu mỗi cột
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
        color="#38bdf8",
    )

  st.pyplot(fig)

# Footer tinh tế cuối trang
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #9ca3af; font-size: 13px;'>✨ Powered"
    " by Streamlit & Python | Designed for Student Management Pro ✨</p>",
    unsafe_allow_html=True,
)
