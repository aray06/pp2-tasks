import psycopg2
import os
import sys
import json
from datetime import datetime

# 1. Настройка кодировок для Windows
os.environ['PGMESSAGES'] = 'English'
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')

from connect import get_connection

# --- 3.1 & 3.4: Добавление контакта и работа с группами ---
def add_full_contact(first_name, last_name, email, birthday, group_name):
    conn = None
    try:
        f_name, l_name = first_name.strip(), last_name.strip()
        mail, grp = email.strip(), group_name.strip()
        
        formatted_date = None
        if birthday and birthday.strip():
            for fmt in ("%d.%m.%Y", "%Y-%m-%d"):
                try:
                    formatted_date = datetime.strptime(birthday.strip(), fmt).strftime("%Y-%m-%d")
                    break
                except ValueError: continue

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO contacts (first_name, last_name, email, birthday) 
            VALUES (%s, %s, %s, %s) ON CONFLICT (first_name, last_name) DO NOTHING;
        """, (f_name, l_name, mail, formatted_date))
        conn.commit()
        cur.execute("CALL move_to_group(%s, %s);", (f_name, grp))
        conn.commit()
        print(f"✅ Success! {f_name} added.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn: conn.close()

# --- 3.3: ИМПОРТ ИЗ JSON (ТОГО ЧЕГО НЕ ХВАТАЛО) ---
def import_from_json(filename="contacts.json"):
    if not os.path.exists(filename):
        print("❌ File not found!")
        return
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        conn = get_connection()
        cur = conn.cursor()

        for entry in data:
            f_name = entry.get('first_name')
            l_name = entry.get('last_name')
            
            # Проверка на дубликат
            cur.execute("SELECT id FROM contacts WHERE first_name=%s AND last_name=%s", (f_name, l_name))
            exists = cur.fetchone()
            
            if exists:
                ans = input(f"❓ Contact {f_name} {l_name} exists. Skip or Overwrite? (s/o): ").lower()
                if ans == 's': continue
                else:
                    cur.execute("DELETE FROM contacts WHERE id=%s", (exists[0],))
                    conn.commit()

            # Добавляем контакт
            add_full_contact(f_name, l_name, entry.get('email'), entry.get('birthday'), entry.get('group'))
            
            # Добавляем телефоны
            for p in entry.get('phones', []):
                add_phone_to_contact(f_name, p['phone'], p['type'])
        
        print("✅ Import finished successfully!")
    except Exception as e:
        print(f"❌ Import Error: {e}")
    finally:
        if conn: conn.close()

# --- 3.4: Добавление телефона ---
def add_phone_to_contact(name, phone, p_type):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("CALL add_phone(%s, %s, %s);", (name.strip(), phone.strip(), p_type.strip()))
        conn.commit()
        # print(f"📞 Phone added to {name}.") # Можно закомментить для чистоты импорта
    except Exception as e:
        print(f"❌ Error adding phone: {e}")
    finally:
        if conn: conn.close()

# --- 3.2: Просмотр с пагинацией ---
def view_with_pagination():
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        page = 0
        limit = 5
        while True:
            cur.execute("""
                SELECT c.first_name, c.last_name, c.email, g.name, c.birthday
                FROM contacts c LEFT JOIN groups g ON c.group_id = g.id
                ORDER BY c.first_name ASC LIMIT %s OFFSET %s
            """, (limit, page * limit))
            rows = cur.fetchall()
            
            if not rows and page == 0:
                print("Phonebook is empty.")
                break
            
            print(f"\n--- Page {page + 1} ---")
            for r in rows:
                print(f"👤 {r[0]} {r[1]} | Email: {r[2]} | Group: {r[3]}")
            
            nav = input("\n[n]ext, [p]rev, [q]uit: ").lower()
            if nav == 'n' and len(rows) == limit: page += 1
            elif nav == 'p': page = max(0, page - 1)
            elif nav == 'q': break
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn: conn.close()

# --- 3.2 & 3.4: Поиск ---
def search_ui(query):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM search_contacts(%s);", (query.strip(),))
        rows = cur.fetchall()
        if not rows: print("Nothing found.")
        else:
            for r in rows:
                print(f"ID: {r[0]} | {r[1]} | {r[2]} | Group: {r[4]}\nPhones: {r[5]}\n" + "-"*40)
    except Exception as e:
        print(f"❌ Search Error: {e}")
    finally:
        if conn: conn.close()

# --- 3.3: Экспорт в JSON ---
def export_to_json(filename="contacts.json"):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.first_name, c.last_name, c.email, c.birthday, g.name,
                   json_agg(json_build_object('phone', p.phone, 'type', p.type)) FILTER (WHERE p.phone IS NOT NULL)
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, g.name;
        """)
        rows = cur.fetchall()
        data = []
        for r in rows:
            data.append({
                "first_name": r[0], "last_name": r[1], "email": r[2],
                "birthday": str(r[3]) if r[3] else None, "group": r[4], "phones": r[5] or []
            })
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"📂 Data exported to {filename}")
    except Exception as e:
        print(f"❌ Export Error: {e}")
    finally:
        if conn: conn.close()

# --- ГЛАВНОЕ МЕНЮ ---
if __name__ == "__main__":
    while True:
        print("\n--- Phonebook Extended (TSIS 1) ---")
        print("1. Add New Contact")
        print("2. Add Phone to existing Contact")
        print("3. View Contacts (Pagination)")
        print("4. Search (Name/Email/Phone)")
        print("5. Import from JSON")  # ДОБАВИЛИ ПУНКТ 5
        print("6. Export to JSON")
        print("0. Exit")
        
        choice = input("\nSelect: ").strip()
        
        if choice == '1':
            add_full_contact(input("First Name: "), input("Last Name: "), 
                             input("Email: "), input("Birthday (DD.MM.YYYY): "), 
                             input("Group: "))
        elif choice == '2':
            add_phone_to_contact(input("Contact First Name: "), 
                                 input("Phone number: "), 
                                 input("Type (mobile/work/home): "))
        elif choice == '3':
            view_with_pagination()
        elif choice == '4':
            search_ui(input("Search query: "))
        elif choice == '5': # ОБРАБОТКА ИМПОРТА
            import_from_json()
        elif choice == '6':
            export_to_json()
        elif choice == '0':
            print("Done! Don't forget to push to GitHub.")
            break