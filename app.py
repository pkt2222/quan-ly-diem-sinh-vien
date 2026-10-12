import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# 1. Cấu hình giao diện tổng thể (Wide layout)
st.set_page_config(
    page_title="Enterprise Student Management Hub",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS tinh chỉnh giao diện hiện đại, chuyên nghiệp
st.markdown(
    """
    <style>
    .main {
        background-color: #f8fafc;
    }
    .metric-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .hero-box {
        background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 20px 25px -5px rgba(79, 70, 229, 0.2);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. Sidebar điều hướng chuyên nghiệp
with st.sidebar:
  st.image(
      "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&auto=format&fit=crop&q=80",
      use_container_width=True,
  )
  st.markdown("### 🎓 **STUDENT HUB PRO**")
  st.markdown("Hệ thống kiểm định & phân tích học lực chuẩn quốc tế.")
  st.markdown("---")

  menu = st.selectbox(
      "📌 CHỌN MODULE QUẢN LÝ",
      [
          "📊 Tổng Quan Hệ Thống (Dashboard)",
          "📋 Quản Trị Cơ Sở Dữ Liệu",
          "🔍 Tra Cứu & Hồ Sơ Cá Nhân",
          "📈 Biểu Đồ Phân Tích Chuyên Sâu",
      ],
  )

  st.markdown("---")
  st.success("🟢 **Trạng thái hệ thống:** Hoạt động ổn định")
  st.markdown("🔒 **Phiên bản:** v3.2 Enterprise")

# 3. Dữ liệu mẫu nâng cao cho 10 sinh viên
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

# Tính điểm Tổng kết hệ 10
df["Tổng kết"] = np.round(
    df["Chuyên cần"] * 0.1 + df["Giữa kỳ"] * 0.3 + df["Cuối kỳ"] * 0.6, 1
)


# Hàm xếp loại chuẩn học thuật chuyên nghiệp
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

# 4. Xây dựng các Module chức năng
if menu == "📊 Tổng Quan Hệ Thống (Dashboard)":
  # Banner chào mừng hiện đại
  st.markdown(
      """
