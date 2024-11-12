import streamlit as st
import pandas as pd
import openpyxl as xl
# ฟังก์ชันโหลดข้อมูลจากไฟล์ Excel
@st.cache_data
def load_excel_data():
    # โหลดข้อมูลจากไฟล์ Excel
    df = pd.read_excel('members.xlsx', sheet_name='Sheet1')  # ปรับตามชื่อแผ่นงานของคุณ
    
    # ลบ comma ในคอลัมน์รหัสพนักงานแล้วแปลงเป็นตัวเลขแบบ integer
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

# ส่วนติดต่อผู้ใช้ใน Streamlit
def main():
    st.title('ระบบค้นหาข้อมูลพนักงาน')

    # โหลดข้อมูลจากไฟล์ Excel
    df = load_excel_data()
    # ช่องให้ผู้ใช้กรอกรหัสพนักงานเพื่อตรวจสอบ
    search_type = st.radio("เลือกวิธีการค้นหา", ('ค้นหาด้วยรหัสพนักงาน', 'ค้นหาด้วยชื่อพนักงาน'))

    if search_type == 'ค้นหาด้วยรหัสพนักงาน':
        employee_id = st.text_input('กรอกรหัสพนักงานที่ต้องการค้นหา')
        if st.button('ค้นหา'):
            if employee_id:
                try:
                    employee_id = int(employee_id)  # แปลงเป็น int
                    result = search_employee(df, employee_id=employee_id)
                    if not result.empty:
                        st.write(f"ผลการค้นหาสำหรับรหัสพนักงาน: {employee_id}")
                        result['รหัสพนักงาน'] = result['รหัสพนักงาน'].astype(str)
                        st.dataframe(result)  # แสดงผลในรูปแบบ DataFrame
                    else:
                        st.warning(f"ไม่พบข้อมูลสำหรับรหัสพนักงาน: {employee_id}")
                except ValueError:
                    st.warning('กรุณากรอกหมายเลขรหัสพนักงานที่ถูกต้อง')
            else:
                st.warning('กรุณากรอกรหัสพนักงาน')

    elif search_type == 'ค้นหาด้วยชื่อพนักงาน':
        employee_name = st.text_input('กรอกชื่อพนักงานที่ต้องการค้นหา')
        if st.button('ค้นหา'):
            if employee_name:
                result = search_employee(df, employee_name=employee_name)
                if not result.empty:
                    st.write(f"ผลการค้นหาสำหรับชื่อพนักงาน: {employee_name}")
                    result['รหัสพนักงาน'] = result['รหัสพนักงาน'].astype(str)
                    st.dataframe(result)  # แสดงผลในรูปแบบ DataFrame
                else:
                    st.warning(f"ไม่พบข้อมูลสำหรับชื่อพนักงาน: {employee_name}")
            else:
                st.warning('กรุณากรอกชื่อพนักงาน')

if __name__ == '__main__':
    main()
