import sqlite3
from database import db


def view_database():
    conn = db.get_connection()
    cursor = conn.cursor()

    # Показать все таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("Таблицы в базе данных:")
    for table in tables:
        print(f" - {table[0]}")

    print("\n" + "=" * 50)

    # Показать данные из таблицы cars
    print("Данные автомобилей:")
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()
    for car in cars:
        print(f"ID: {car[0]}, Марка: {car[1]}, Модель: {car[2]}, Год: {car[3]}, Цена: ${car[4]}")

    print("\n" + "=" * 50)

    # Показать данные из таблицы contacts
    print("Заявки:")
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    for contact in contacts:
        print(f"ID: {contact[0]}, Имя: {contact[1]}, Email: {contact[2]}, Телефон: {contact[3]}")

    conn.close()


if __name__ == "__main__":
    view_database()