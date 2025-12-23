import mysql.connector
from datetime import date

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="290605",   
        database="medical_service",
        port=3307
    )

def add_patients():
    conn = connect_db()
    cursor = conn.cursor()
    for i in range(3):
        print(f"\nNhập bệnh nhân {i+1}")
        name = input("Tên: ")
        dob = input("Ngày sinh (YYYY-MM-DD): ")
        gender = input("Giới tính: ")
        address = input("Địa chỉ: ")
        cursor.execute(
            "INSERT INTO patients(full_name, date_of_birth, gender, address) VALUES (%s,%s,%s,%s)",
            (name, dob, gender, address)
        )
    conn.commit()
    conn.close()
    print("✔ Đã thêm 3 bệnh nhân")

def add_doctors():
    conn = connect_db()
    cursor = conn.cursor()
    for i in range(5):
        print(f"\nNhập bác sĩ {i+1}")
        name = input("Tên bác sĩ: ")
        spec = input("Chuyên khoa: ")
        cursor.execute(
            "INSERT INTO doctors(full_name, specialization) VALUES (%s,%s)",
            (name, spec)
        )
    conn.commit()
    conn.close()
    print("✔ Đã thêm 5 bác sĩ")

def add_appointments():
    conn = connect_db()
    cursor = conn.cursor()
    for i in range(3):
        print(f"\nNhập lịch hẹn {i+1}")
        pid = int(input("Patient ID: "))
        did = int(input("Doctor ID: "))
        dt = input("Ngày hẹn (YYYY-MM-DD HH:MM:SS): ")
        reason = input("Lý do: ")
        cursor.execute(
            "INSERT INTO appointments(patient_id, doctor_id, appointment_date, reason) VALUES (%s,%s,%s,%s)",
            (pid, did, dt, reason)
        )
    conn.commit()
    conn.close()
    print("✔ Đã thêm 3 lịch hẹn")

def report_all():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.full_name, p.date_of_birth, p.gender, p.address,
               d.full_name, a.reason, a.appointment_date
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
    """)
    rows = cursor.fetchall()

    print("\nNo | Patient | Birthday | Gender | Address | Doctor | Reason | Date")
    print("-"*90)
    for i, r in enumerate(rows, start=1):
        print(f"{i} | {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]}")
    conn.close()

def appointments_today():
    conn = connect_db()
    cursor = conn.cursor()
    today = date.today()
    cursor.execute("""
        SELECT p.address, p.full_name, p.date_of_birth, p.gender,
               d.full_name, a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE DATE(a.appointment_date) = %s
    """, (today,))
    rows = cursor.fetchall()

    print("\nAddress | Patient | Birthday | Gender | Doctor | Status")
    print("-"*70)
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]}")
    conn.close()

def main():
    while True:
        print("\n1. Add 3 patients")
        print("2. Add 5 doctors")
        print("3. Add 3 appointments")
        print("4. Report all appointments")
        print("5. Appointments today")
        print("0. Exit")
        c = input("Choose: ")

        if c == "1": add_patients()
        elif c == "2": add_doctors()
        elif c == "3": add_appointments()
        elif c == "4": report_all()
        elif c == "5": appointments_today()
        elif c == "0": break
        else: print("Sai lựa chọn")

if __name__ == "__main__":
    main()
