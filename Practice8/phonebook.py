import psycopg2
import os
import csv
import sys

# 1. Настройка окружения для Windows (кодировка и сообщения)
os.environ['PGMESSAGES'] = 'English'
os.environ['PGCLIENTENCODING'] = 'UTF8'
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 2. Параметры подключения
params = {
    "host": "localhost",
    "database": "phonebook_db",
    "user": "postgres",
    "password": "qazxcvfdt",
    "port": "5433" 
}

def add_contact(name, phone):
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
        conn.commit()
        print(f"Success! Contact {name} added.")
        cur.close()
    except Exception as e:
        print(f"Detailed Error in Add: {e}")
    finally:
        if conn: conn.close()

def search_contacts(pattern):
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
        results = cur.fetchall()
        print(f"\nSearch results for '{pattern}':")
        if not results:
            print("No contacts found.")
        else:
            for row in results:
                print(row)
        cur.close()
    except Exception as e:
        print(f"Search Error: {e}")
    finally:
        if conn: conn.close()

def delete_contact(name_or_phone):
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("DELETE FROM contacts WHERE name = %s OR phone = %s", (name_or_phone, name_or_phone))
        conn.commit()
        print(f"Contact {name_or_phone} deleted if it existed.")
        cur.close()
    except Exception as e:
        print(f"Delete Error: {e}")
    finally:
        if conn: conn.close()

def upload_from_csv(file_name):
    """Читает CSV файл и добавляет контакты в базу"""
    if not os.path.exists(file_name):
        print(f"File {file_name} not found!")
        return
    try:
        with open(file_name, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    name, phone = row
                    add_contact(name.strip(), phone.strip())
        print(f"Upload from {file_name} completed.")
    except Exception as e:
        print(f"CSV Error: {e}")

# --- ГЛАВНОЕ МЕНЮ ---
if __name__ == "__main__":
    while True:
        print("\n--- Phonebook Menu ---")
        print("1. Add/Update Contact")
        print("2. Search Contact")
        print("3. Delete Contact")
        print("4. Upload from CSV")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            add_contact(name, phone)
        elif choice == '2':
            pattern = input("Enter search pattern: ")
            search_contacts(pattern)
        elif choice == '3':
            target = input("Enter name or phone to delete: ")
            delete_contact(target)
        elif choice == '4':
            filename = input("Enter csv filename (e.g., contacts.csv): ")
            upload_from_csv(filename)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")