import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# 1. Cấu hình tiêu đề trang
st.set_page_config(
    page_title="Quản Lý Điểm Sinh Viên", page_icon="📚", layout="centered"
)

st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("Ứng dụng quản lý và thống kê điểm số học tập của sinh viên.")

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

# 3. Hiển thị bảng điểm của 10 sinh viên
st.subheader("📋 Bảng điểm chi tiết 10 sinh viên")
st.dataframe(df, use_container_width=True)

# 4. Thống kê chung
st.subheader("📊 Thống kê chung")
dtb_lop = np.round(df["Tổng kết"].mean(), 2)
so_sinh_vien_dat = len(df[df["Tổng kết"] >= 5.0])

col1, col2, col3 = st.columns(3)
with col1:
  st.metric(label="Điểm TB của lớp", value=dtb_lop)
with col2:
  st.metric(label="Số sinh viên đạt (>=5.0)", value=f"{so_sinh_vien_dat}/10")
with col3:
  max_sv = df.loc[df["Tổng kết"].idxmax()]
  st.metric(label="Điểm TK cao nhất", value=f"{max_sv['Tổng kết']}")

# Sinh viên cao nhất và thấp nhất
sv_cao_nhat = df.loc[df["Tổng kết"].idxmax()]["Họ tên"]
sv_thap_nhat = df.loc[df["Tổng kết"].idxmin()]["Họ tên"]

st.info(
    f"🏆 **Sinh viên có điểm tổng kết cao nhất:** {sv_cao_nhat} ("
    f"{df.loc[df['Tổng kết'].idxmax()]['Tổng kết']} điểm)"
)
st.warning(
    f"⚠️ **Sinh viên có điểm tổng kết thấp nhất:** {sv_thap_nhat} ("
    f"{df.loc[df['Tổng kết'].idxmin()]['Tổng kết']} điểm)"
)

# 5. Tạo Selectbox chọn sinh viên
st.subheader("🔍 Tra cứu điểm theo sinh viên")
selected_student = st.selectbox("Chọn tên sinh viên:", df["Họ tên"])

student_info = df[df["Họ tên"] == selected_student].iloc[0]

st.write(f"Kết quả học tập của **{selected_student}**:")
col_a, col_b, col_c, col_d, col_e = st.columns(5)
col_a.metric("Chuyên cần", student_info["Chuyên cần"])
col_b.metric("Giữa kỳ", student_info["Giữa kỳ"])
col_c.metric("Cuối kỳ", student_info["Cuối kỳ"])
col_d.metric("Tổng kết", student_info["Tổng kết"])
col_e.metric("Xếp loại", student_info["Xếp loại"])

# 6. Biểu đồ cột
st.subheader("📈 Biểu đồ cột điểm tổng kết của lớp")
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df["Họ tên"], df["Tổng kết"], color="skyblue", edgecolor="navy")
ax.set_xlabel("Họ và tên sinh viên")
ax.set_ylabel("Điểm Tổng kết")
ax.set_title("Biểu đồ điểm Tổng kết 10 sinh viên")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)

# 7. Chân trang (Footer)
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: small; color: gray;'>Ứng dụng"
    " được phát triển bởi: [Điền Họ Tên Bạn] - [Điền MSSV Bạn]</p>",
    unsafe_allow_html=True,
)
