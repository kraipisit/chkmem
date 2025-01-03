import streamlit as st
import pandas as pd

# ตั้งค่าการแสดงผลของหน้าเว็บ
st.set_page_config(
    page_title="ระบบค้นหาข้อมูลพนักงาน",
    page_icon="📋",
    layout="wide"
)

# ฟังก์ชันโหลดข้อมูลจากไฟล์ Excel
@st.cache_data
def load_excel_data():
    df = pd.read_excel('members.xlsx', sheet_name='Sheet1')  # ปรับตามชื่อแผ่นงานของคุณ
    df['รหัสพนักงาน'] = df['รหัสพนักงาน'].astype(str).str.replace(',', '', regex=True).astype(int)
    return df

# ฟังก์ชันค้นหาข้อมูลพนักงานตามรหัสพนักงานหรือชื่อพนักงาน
def search_employee(df, employee_id=None, employee_name=None):
    if employee_id:
        # ค้นหาด้วยรหัสพนักงาน
        result = df[df['รหัสพนักงาน'] == employee_id]
    elif employee_name:
        # ค้นหาด้วยชื่อพนักงาน (ค้นหาแบบที่มีชื่อคล้ายกันด้วย .str.contains)
        result = df[df['ชื่อ'].str.contains(employee_name, case=False, na=False)]
    else:
        result = pd.DataFrame()  # ถ้าไม่มีการป้อนข้อมูล, คืนค่าข้อมูลว่าง
    return result

# ฟังก์ชันเพิ่มสไตล์ CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main Application
def main():
    # เพิ่ม CSS เพื่อปรับแต่ง
    local_css("styles.css")

    st.title("📋 ระบบค้นหาข้อมูลพนักงาน")
    st.markdown("### ค้นหาพนักงานง่ายและรวดเร็ว")

    # โหลดข้อมูล
    df = load_excel_data()

    # การค้นหา
    with st.sidebar:
        st.header("🔍 เลือกวิธีการค้นหา")
        search_type = st.radio("", ('ค้นหาด้วยรหัสพนักงาน', 'ค้นหาด้วยชื่อพนักงาน'))

    col1, col2 = st.columns([3, 1])

    with col1:
        if search_type == 'ค้นหาด้วยรหัสพนักงาน':
            employee_id = st.text_input('กรอกรหัสพนักงานที่ต้องการค้นหา')
            if st.button('ค้นหา'):
                if employee_id:
                    try:
                        employee_id = int(employee_id)
                        result = search_employee(df, employee_id=employee_id)
                        if not result.empty:
                            st.success(f"พบผลการค้นหาสำหรับรหัสพนักงาน: {employee_id}")
                            result['รหัสพนักงาน'] = result['รหัสพนักงาน'].astype(str)
                            st.dataframe(result, use_container_width=True)
                        else:
                            st.warning(f"ไม่พบข้อมูลสำหรับรหัสพนักงาน: {employee_id}")
                    except ValueError:
                        st.error('กรุณากรอกหมายเลขรหัสพนักงานที่ถูกต้อง')
                else:
                    st.error('กรุณากรอกรหัสพนักงาน')

        elif search_type == 'ค้นหาด้วยชื่อพนักงาน':
            employee_name = st.text_input('กรอกชื่อพนักงานที่ต้องการค้นหา')
            if st.button('ค้นหา'):
                if employee_name:
                    result = search_employee(df, employee_name=employee_name)
                    if not result.empty:
                        st.success(f"พบผลการค้นหาสำหรับชื่อพนักงาน: {employee_name}")
                        result['รหัสพนักงาน'] = result['รหัสพนักงาน'].astype(str)
                        st.dataframe(result, use_container_width=True)
                    else:
                        st.warning(f"ไม่พบข้อมูลสำหรับชื่อพนักงาน: {employee_name}")
                else:
                    st.error('กรุณากรอกชื่อพนักงาน')

if __name__ == '__main__':
    main()