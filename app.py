import streamlit as st
import pandas as pd

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 APP TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.write("Tính tiền lãi theo **lãi đơn** hoặc **lãi kép**")

st.divider()

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(number):
    return f"{number:,.0f} VNĐ".replace(",", ".")


# =========================
# NHẬP THÔNG TIN
# =========================

st.subheader("📌 Thông tin tiền gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.01
)

hinh_thuc_lai = st.selectbox(
    "Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_lanh = st.selectbox(
    "Hình thức lãnh lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

# =========================
# NÚT TÍNH
# =========================

if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    lai_suat_nam = lai_suat / 100

    # Số tháng
    so_thang = int(ky_han)

    # =========================
    # XÁC ĐỊNH SỐ KỲ NHẬN LÃI
    # =========================

    if hinh_thuc_lanh == "Lãnh lãi theo tháng":
        so_ky = so_thang
        thang_moi_ky = 1
        ten_ky = "Tháng"

    elif hinh_thuc_lanh == "Lãnh lãi theo quý":
        so_ky = so_thang // 3

        # Nếu kỳ hạn không chia hết cho 3,
        # phần tháng còn lại sẽ được tính vào cuối kỳ.
        thang_moi_ky = 3
        ten_ky = "Quý"

    else:
        so_ky = 1
        thang_moi_ky = so_thang
        ten_ky = "Cuối kỳ"

    # =========================
    # TÍNH LÃI ĐƠN
    # =========================

    if hinh_thuc_lai == "Lãi đơn":

        # Tổng lãi:
        # I = P * r * t
        tong_lai = so_tien * lai_suat_nam * (so_thang / 12)

        # Lãi định kỳ
        if hinh_thuc_lanh == "Lãnh lãi theo tháng":
            lai_dinh_ky = so_tien * lai_suat_nam / 12

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":
            lai_dinh_ky = so_tien * lai_suat_nam / 4

        else:
            lai_dinh_ky = tong_lai

        tong_tien = so_tien + tong_lai

        # =========================
        # TẠO BẢNG CHI TIẾT
        # =========================

        danh_sach = []

        if hinh_thuc_lanh == "Lãnh lãi theo tháng":

            for i in range(1, so_thang + 1):
                danh_sach.append({
                    "Kỳ": f"Tháng {i}",
                    "Tiền lãi kỳ này": lai_dinh_ky,
                    "Tổng lãi lũy kế": lai_dinh_ky * i,
                    "Tổng tiền": so_tien + lai_dinh_ky * i
                })

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":

            for i in range(1, so_ky + 1):
                danh_sach.append({
                    "Kỳ": f"Quý {i}",
                    "Tiền lãi kỳ này": lai_dinh_ky,
                    "Tổng lãi lũy kế": lai_dinh_ky * i,
                    "Tổng tiền": so_tien + lai_dinh_ky * i
                })

        else:
            danh_sach.append({
                "Kỳ": "Cuối kỳ",
                "Tiền lãi kỳ này": tong_lai,
                "Tổng lãi lũy kế": tong_lai,
                "Tổng tiền": tong_tien
            })

    # =========================
    # TÍNH LÃI KÉP
    # =========================

    else:

        danh_sach = []

        # Lãi kép theo tháng
        if hinh_thuc_lanh == "Lãnh lãi theo tháng":

            lai_suat_ky = lai_suat_nam / 12
            tien_hien_tai = so_tien

            for i in range(1, so_thang + 1):

                tien_lai = tien_hien_tai * lai_suat_ky
                tien_hien_tai += tien_lai

                danh_sach.append({
                    "Kỳ": f"Tháng {i}",
                    "Tiền lãi kỳ này": tien_lai,
                    "Tổng lãi lũy kế": tien_hien_tai - so_tien,
                    "Tổng tiền": tien_hien_tai
                })

            tong_tien = tien_hien_tai
            tong_lai = tong_tien - so_tien
            lai_dinh_ky = danh_sach[-1]["Tiền lãi kỳ này"]

        # =========================
        # LÃI KÉP THEO QUÝ
        # =========================

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":

            lai_suat_ky = lai_suat_nam / 4
            tien_hien_tai = so_tien

            so_quy = so_thang // 3
            thang_du = so_thang % 3

            for i in range(1, so_quy + 1):

                tien_lai = tien_hien_tai * lai_suat_ky
                tien_hien_tai += tien_lai

                danh_sach.append({
                    "Kỳ": f"Quý {i}",
                    "Tiền lãi kỳ này": tien_lai,
                    "Tổng lãi lũy kế": tien_hien_tai - so_tien,
                    "Tổng tiền": tien_hien_tai
                })

            # Nếu còn tháng lẻ
            if thang_du > 0:

                lai_le = tien_hien_tai * lai_suat_nam * (thang_du / 12)
                tien_hien_tai += lai_le

                danh_sach.append({
                    "Kỳ": f"{thang_du} tháng còn lại",
                    "Tiền lãi kỳ này": lai_le,
                    "Tổng lãi lũy kế": tien_hien_tai - so_tien,
                    "Tổng tiền": tien_hien_tai
                })

            tong_tien = tien_hien_tai
            tong_lai = tong_tien - so_tien

            if danh_sach:
                lai_dinh_ky = danh_sach[-1]["Tiền lãi kỳ này"]
            else:
                lai_dinh_ky = 0

        # =========================
        # LÃNH LÃI CUỐI KỲ
        # =========================

        else:

            # Lãi kép theo tháng
            lai_suat_thang = lai_suat_nam / 12

            tong_tien = so_tien * (
                (1 + lai_suat_thang) ** so_thang
            )

            tong_lai = tong_tien - so_tien
            lai_dinh_ky = tong_lai

            danh_sach.append({
                "Kỳ": "Cuối kỳ",
                "Tiền lãi kỳ này": tong_lai,
                "Tổng lãi lũy kế": tong_lai,
                "Tổng tiền": tong_tien
            })

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================

    st.divider()
    st.subheader("📊 KẾT QUẢ TÍNH TOÁN")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            format_money(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_lai)
        )

    st.metric(
        "💰 Tổng tiền gốc + lãi",
        format_money(tong_tien)
    )

    # =========================
    # THÔNG TIN TÓM TẮT
    # =========================

    st.info(
        f"""
        **Thông tin khoản gửi**

        - Số tiền gốc: **{format_money(so_tien)}**
        - Kỳ hạn: **{so_thang} tháng**
        - Lãi suất: **{lai_suat:.2f}%/năm**
        - Phương pháp: **{hinh_thuc_lai}**
        - Hình thức lãnh: **{hinh_thuc_lanh}**
        """
    )

    # =========================
    # BẢNG CHI TIẾT
    # =========================

    st.subheader("📋 Chi tiết tiền lãi")

    df = pd.DataFrame(danh_sach)

    # Định dạng tiền trong bảng
    df_hien_thi = df.copy()

    for cot in [
        "Tiền lãi kỳ này",
        "Tổng lãi lũy kế",
        "Tổng tiền"
    ]:
        if cot in df_hien_thi.columns:
            df_hien_thi[cot] = df_hien_thi[cot].apply(format_money)

    st.dataframe(
        df_hien_thi,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # CÔNG THỨC
    # =========================

    with st.expander("📚 Xem công thức tính"):

        if hinh_thuc_lai == "Lãi đơn":

            st.markdown("""
            ### Lãi đơn

            **Tiền lãi:**

            `I = P × r × t`

            Trong đó:

            - `P`: Số tiền gốc
            - `r`: Lãi suất năm
            - `t`: Thời gian gửi tính theo năm

            **Tổng tiền:**

            `A = P + I`
            """)

        else:

            st.markdown("""
            ### Lãi kép

            **Công thức:**

            `A = P × (1 + r)ⁿ`

            Trong đó:

            - `P`: Số tiền gốc
            - `r`: Lãi suất mỗi kỳ
            - `n`: Số kỳ tính lãi
            - `A`: Tổng tiền gốc và lãi

            **Tổng tiền lãi:**

            `I = A - P`
            """)

# =========================
# CHÂN TRANG
# =========================

st.divider()

st.caption(
    "💡 Công cụ tính toán mang tính tham khảo. "
    "Lãi suất thực tế có thể phụ thuộc vào quy định của từng ngân hàng."
)
