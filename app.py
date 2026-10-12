import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# 1. Cấu hình giao diện rộng (Wide layout)
st.set_page_config(
    page_title="Hệ Thống Quản Lý Điểm Sinh Viên", page_icon="🎓", layout="wide"
)

# Tiêu đề chính ứng dụng
st.title("🎓 HỆ THỐNG QUẢN LÝ VÀ PHÂN TÍCH ĐIỂM SINH VIÊN")
st.markdown(
    "Ứng dụng hỗ trợ theo dõi, tra cứu và thống kê kết quả học tập trực quan."
)
st.markdown("---")

# 2. Tạo dữ liệu mẫu cho 10 sinh viên
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
    "Chuyên cần": np.random.randint(7, 10, 10).astype(float),
    "Giữa kỳ": np.round(np.random.uniform(4.0, 9.5, 10), 1),
    "Cuối kỳ": np.round(np.random.uniform(4.0, 10.0, 10), 1),
}

df = pd.DataFrame(data)

# Tính điểm Tổng kết
df["Tổng kết"] = np.round(
    df["Chuyên cần"] * 0.1 + df["Giữa kỳ"] * 0.3 + df["Cuối kỳ"] * 0.6, 1
)


# Hàm xếp loại
def xep_loai(diem):
  if diem >= 8.5:
    return "Giỏi"
  elif diem >= 7.0:
    return "Khá"
  elif diem >= 5.0:
    return "Trung bình"
  else:
    return "Yếu"


df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# 3. Phân chia giao diện thành các Tabs hiện đại
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Tổng Quan & Thống Kê",
    "📋 Bảng Điểm Chi Tiết",
    "🔍 Tra Cứu Sinh Viên",
    "📈 Biểu Đồ Phân Tích",
])

with tab1:
  st.subheader("📌 Các chỉ số tổng quan của lớp")
  dtb_lop = np.round(df["Tổng kết"].mean(), 2)
  so_sinh_vien_dat = len(df[df["Tổng kết"] >= 5.0])
  max_sv = df.loc[df["Tổng kết"].idxmax()]
  min_sv = df.loc[df["Tổng kết"].idxmin()]

  c1, c2, c3, c4 = st.columns(4)
  c1.metric(
      label="📚 Tổng số sinh viên", value=f"{len(df)} sinh viên", delta="100%"
  )
  c2.metric(label="📈 Điểm trung bình lớp", value=f"{dtb_lop} / 10")
  c3.metric(
      label="✅ Số sinh viên đạt (>=5.0)",
      value=f"{so_sinh_vien_dat} sinh viên",
  )
  c4.metric(label="🏆 Điểm tổng kết cao nhất", value=f"{max_sv['Tổng kết']}")

  st.markdown("---")
  col_info1, col_info2 = st.columns(2)
  with col_info1:
    st.success(
        f"🌟 **Sinh viên xuất sắc nhất:** {max_sv['Họ tên']} với tổng kết"
        f" **{max_sv['Tổng kết']}** điểm."
    )
  with col_info2:
    st.warning(
        f"⚠️ **Sinh viên cần cố gắng thêm:** {min_sv['Họ tên']} với tổng kết"
        f" **{min_sv['Tổng kết']}** điểm."
    )

with tab2:
  st.subheader("📋 Bảng điểm toàn bộ sinh viên")
  st.dataframe(df, use_container_width=True)

with tab3:
  st.subheader("🔍 Tra cứu kết quả học tập cá nhân")
  selected_student = st.selectbox(
      "Chọn hoặc gõ tên sinh viên cần xem:", df["Họ tên"]
  )

  student_info = df[df["Họ tên"] == selected_student].iloc[0]

  st.info(f"Đang hiển thị kết quả chi tiết của: **{selected_student}**")
  sc1, sc2, sc3, sc4, sc5 = st.columns(5)
  sc1.metric("Chuyên cần", student_info["Chuyên cần"])
  sc2.metric("Giữa kỳ", student_info["Giữa kỳ"])
  sc3.metric("Cuối kỳ", student_info["Cuối kỳ"])
  sc4.metric("Tổng kết", student_info["Tổng kết"])
  sc5.metric("Xếp loại", student_info["Xếp loại"])

with tab4:
  st.subheader("📈 Biểu đồ trực quan điểm tổng kết lớp")
  fig, ax = plt.subplots(figsize=(10, 4.5))
  bars = ax.bar(
      df["Họ tên"],
      df["Tổng kết"],
      color="#4F46E5",
      edgecolor="#312E81",
      alpha=0.85,
  )
  ax.set_xlabel("Họ và tên sinh viên", fontweight="bold")
  ax.set_ylabel("Điểm Tổng kết", fontweight="bold")
  ax.set_title("Biểu đồ cột điểm tổng kết", fontsize=14, fontweight="bold")
  plt.xticks(rotation=30, ha="right")
  ax.grid(axis="y", linestyle="--", alpha=0.5)

  # Hiển thị số điểm trên đầu cột
  for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f"{height}",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),  # 3 points vertical offset
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=9,
    )

  st.pyplot(fig)

# 4. Chân trang (Footer)
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 14px;'>Được phát"
    " triển bởi [Phan Khải Trí] - [066208002686] | Ứng dụng Quản lý Điểm Sinh"
    " Viên</p>",
    unsafe_allow_html=True,
)
