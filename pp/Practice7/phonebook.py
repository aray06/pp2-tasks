import csv
from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# 1. Вставка из CSV
def import_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING;", row)
    conn.commit()
    print("Данные из CSV импортированы.")
    cur.close()
    conn.close()

# 2. Ввод из консоли
def add_contact():
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s);", (name, phone))
        conn.commit()
        print("Контакт сохранен!")
    except Exception as e:
        print(f"Ошибка (возможно, такой номер уже есть): {e}")
    finally:
        cur.close()
        conn.close()

# 3. Обновление
def update_contact():
    target = input("Чьи данные обновить? (Введите имя): ")
    new_phone = input("Введите новый номер телефона: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s;", (new_phone, target))
    conn.commit()
    print("Данные обновлены.")
    cur.close()
    conn.close()

# 4. Фильтры (Поиск)
def find_contacts():
    query = input("Введите имя или начало телефона для поиска: ")
    conn = get_connection()
    cur = conn.cursor()
    # Используем ILIKE для поиска по части слова и игнорирования регистра
    cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s OR phone LIKE %s;", (f'%{query}%', f'{query}%'))
    rows = cur.fetchall()
    for row in rows:
        print(f"ID: {row[0]} | Имя: {row[1]} | Тел: {row[2]}")
    cur.close()
    conn.close()

# 5. Удаление
def delete_contact():
    info = input("Введите имя или номер для удаления: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE name = %s OR phone = %s;", (info, info))
    conn.commit()
    print("Контакт удален (если он существовал).")
    cur.close()
    conn.close()

# 5. Удаление
def delete_contact():
    info = input("Введите имя или номер для удаления: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE name = %s OR phone = %s;", (info, info))
    conn.commit()
    print("Контакт удален (если он существовал).")
    cur.close()
    conn.close()

# ТЕПЕРЬ ОНА НА СВОЕМ МЕСТЕ
def get_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook ORDER BY id;")
    rows = cur.fetchall()
    
    if not rows:
        print("\n[!] Телефонная книга пуста.")
    else:
        print("\n--- СПИСОК ВСЕХ КОНТАКТОВ ---")
        for row in rows:
            print(f"ID: {row[0]} | Имя: {row[1]} | Тел: {row[2]}")
            
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_table()
    
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Загрузить из CSV")
        print("2. Добавить контакт вручную")
        print("3. Найти контакт (поиск)")
        print("4. Обновить телефон")
        print("5. Удалить контакт")
        print("6. Показать всех")
        print("0. Выход")
        
        choice = input("\nВыбери действие: ")

        if choice == '1':
            import_from_csv('contacts.csv')
        elif choice == '2':
            add_contact()
        elif choice == '3':
            find_contacts()
        elif choice == '4':
            update_contact()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            get_users() # Используем твою функцию из первой части или допиши её
        elif choice == '0':
            print("Пока!")
            break
        else:
            print("Нет такого варианта, попробуй еще раз.")