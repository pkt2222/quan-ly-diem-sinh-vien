import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# 1. Cấu hình giao diện tổng thể
st.set_page_config(
    page_title="Enterprise Student Management Hub",
    page_icon="🛡️",
    layout="wide",
)

# Custom CSS giao diện
st.markdown(
    """
    <style>
    .main { background-color: #f8fafc; }
    .hero-box {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. Sidebar điều hướng
with st.sidebar:
  st.markdown("### 🎓 **STUDENT HUB PRO**")
  st.markdown("Hệ thống quản lý học lực chuyên nghiệp.")
  st.markdown("---")
  menu = st.selectbox(
      "📌 CHỌN MODULE QUẢN LÝ",
      [
          "📊 Tổng Quan Dashboard",
          "📋 Quản Trị Cơ Sở Dữ Liệu",
          "🔍 Tra Cứu & Hồ Sơ Cá Nhân",
          "📈 Biểu Đồ Phân Tích",
      ],
  )
  st.markdown("---")
  st.success("🟢 Trạng thái: Hoạt động ổn định")

# 3. Dữ liệu mẫu 10 sinh viên
np.random.seed(42)
data = {
    "Mã SV": [f"SV{101+i}" for i in range(10)],
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
    return "⚠️ Cảnh báo"


df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# 4. Các Module hiển thị
if menu == "📊 Tổng Quan Dashboard":
  st.markdown(
      """
        <div class="hero-box">
            <h2>🚀 Cổng Quản Trị Học Tập Tổng Quan</h2>
            <p>Hệ thống tự động tổng hợp và phân tích trực quan kết quả học tập của sinh viên.</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  dtb_lop = np.round(df["Tổng kết"].mean(), 2)
  so_sv_dat = len(df[df["Tổng kết"] >= 5.0])
  max_sv = df.loc[df["Tổng kết"].idxmax()]
  min_sv = df.loc[df["Tổng kết"].idxmin()]

  col1, col2, col3, col4 = st.columns(4)
  col1.metric("👥 Tổng Sĩ Số", f"{len(df)} SV")
  col2.metric("⭐ Điểm Trung Bình", f"{dtb_lop} / 10")
  col3.metric("✅ Tỷ Lệ Đạt", f"{(so_sv_dat/len(df))*100}%")
  col4.metric("🏆 Điểm Cao Nhất", f"{max_sv['Tổng kết']}")

  st.markdown("---")
  c1, c2 = st.columns(2)
  c1.success(
      f"🥇 **Thủ khoa:** {max_sv['Họ tên']} với điểm tổng kết"
      f" **{max_sv['Tổng kết']}**."
  )
  c2.warning(
      f"⚠️ **Cần hỗ trợ:** {min_sv['Họ tên']} với điểm tổng kết"
      f" **{min_sv['Tổng kết']}**."
  )

elif menu == "📋 Quản Trị Cơ Sở Dữ Liệu":
  st.title("📋 BẢNG ĐIỂM CHI TIẾT TOÀN KHÓA")
  keyword = st.text_input("🔍 Tìm kiếm sinh viên theo tên hoặc Mã SV:", "")
  if keyword:
    filtered = df[
        df["Họ tên"].str.contains(keyword, case=False, na=False)
        | df["Mã SV"].str.contains(keyword, case=False, na=False)
    ]
    st.dataframe(filtered, use_container_width=True)
  else:
    st.dataframe(df, use_container_width=True)

elif menu == "🔍 Tra Cứu & Hồ Sơ Cá Nhân":
  st.title("🔍 HỒ SƠ ĐÁNH GIÁ NĂNG LỰC CÁ NHÂN")
  selected_student = st.selectbox("👉 Chọn sinh viên:", df["Họ tên"])
  s_info = df[df["Họ tên"] == selected_student].iloc[0]

  m1, m2, m3, m4 = st.columns(4)
  m1.metric("📘 Chuyên cần", s_info["Chuyên cần"])
  m2.metric("✍️ Giữa kỳ", s_info["Giữa kỳ"])
  m3.metric("📝 Cuối kỳ", s_info["Cuối kỳ"])
  m4.metric("📊 Tổng kết", s_info["Tổng kết"])
  st.markdown(f"### 🏅 Xếp loại học lực: **{s_info['Xếp loại']}**")

elif menu == "📈 Biểu Đồ Phân Tích":
  st.title("📈 BIỂU ĐỒ PHÂN TÍCH ĐIỂM SỐ")
  fig, ax = plt.subplots(figsize=(10, 4.5))
  bars = ax.bar(
      df["Họ tên"],
      df["Tổng kết"],
      color="#3b82f6",
      edgecolor="#1d4ed8",
      linewidth=1.2,
  )
  ax.set_ylabel("Điểm Tổng Kết")
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
    )
  st.pyplot(fig)

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Enterprise Student Hub"
    " Management System</p>",
    unsafe_allow_html=True,
)
