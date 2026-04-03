import psycopg2
import csv
from Practice8.config import DB_CONFIG

# --- Функции для работы с БД ---

def add_contact(first_name, last_name, phone):
    """1. Добавление контакта через консоль"""
    sql = "INSERT INTO contacts (first_name, last_name, phone_number) VALUES (%s, %s, %s);"
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name, last_name, phone))
                conn.commit()
                print("✅ Контакт успешно добавлен!")
    except Exception as e:
        print(f"❌ Ошибка при добавлении: {e}")

def update_contact():
    """2. Обновление номера телефона по имени"""
    name = input("Кого будем искать для обновления? (Введите имя): ")
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT first_name, last_name, phone_number FROM contacts WHERE first_name = %s", (name,))
                contact = cur.fetchone()
                
                if contact:
                    print(f"✅ Нашел: {contact[0]} {contact[1]}, текущий номер: {contact[2]}")
                    new_phone = input(f"Введите новый номер для {name}: ")
                    cur.execute("UPDATE contacts SET phone_number = %s WHERE first_name = %s", (new_phone, name))
                    conn.commit()
                    print("🚀 Данные успешно обновлены!")
                else:
                    print(f"❌ Контакт с именем '{name}' не найден.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def query_contacts(search_term):
    """3. Поиск контактов (фильтр по имени или номеру)"""
    sql = "SELECT * FROM contacts WHERE first_name LIKE %s OR phone_number LIKE %s;"
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (f'%{search_term}%', f'%{search_term}%'))
                results = cur.fetchall()
                print("\n--- Результаты поиска ---")
                for row in results:
                    print(f"ID: {row[0]} | Имя: {row[1]} {row[2]} | Тел: {row[3]}")
    except Exception as e:
        print(f"❌ Ошибка поиска: {e}")

def delete_contact(identifier):
    """4. Удаление контакта по имени или номеру"""
    sql = "DELETE FROM contacts WHERE first_name = %s OR phone_number = %s;"
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (identifier, identifier))
                conn.commit()
                print(f"🗑️ Контакт {identifier} удален!")
    except Exception as e:
        print(f"❌ Ошибка при удалении: {e}")

def show_all_contacts():
    """5. Показать все контакты из базы данных"""
    sql = "SELECT * FROM contacts ORDER BY id;"
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                results = cur.fetchall()
                print("\n--- СПИСОК ВСЕХ КОНТАКТОВ ---")
                if not results:
                    print("Список пуст.")
                for row in results:
                    print(f"ID: {row[0]} | {row[1]} {row[2]} | Тел: {row[3]}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def import_from_csv(filename):
    """6. Загрузка новых контактов из CSV файла в БД"""
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Если в CSV есть заголовки, убери решетку ниже:
            # next(reader) 
            
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cur:
                    for row in reader:
                        if len(row) < 3: continue
                        # Используем ON CONFLICT, чтобы не было ошибок при дубликатах номеров
                        sql = """
                        INSERT INTO contacts (first_name, last_name, phone_number)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (phone_number) DO NOTHING;
                        """
                        cur.execute(sql, (row[0], row[1], row[2]))
                conn.commit()
        print(f"✅ Данные из '{filename}' успешно загружены в базу!")
    except FileNotFoundError:
        print(f"❌ Файл '{filename}' не найден. Создайте его в папке с проектом.")
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")

# --- Главное меню ---

def main():
    while True:
        print("\n--- PHONEBOOK APP (PostgreSQL) ---")
        print("1. Добавить контакт (Консоль)")
        print("2. Обновить контакт (Имя -> Новый номер)")
        print("3. Поиск (Имя или Номер)")
        print("4. Удалить контакт (Имя или Номер)")
        print("5. Показать все контакты")
        print("6. Загрузить новых людей из CSV")
        print("0. Выход")
        
        choice = input("\nВыберите действие: ")

        if choice == '1':
            add_contact(input("Имя: "), input("Фамилия: "), input("Телефон: "))
        elif choice == '2':
            update_contact() 
        elif choice == '3':
            query_contacts(input("Кого ищем? "))
        elif choice == '4':
            delete_contact(input("Введите имя или номер для удаления: "))
        elif choice == '5':
            show_all_contacts()
        elif choice == '6':
            import_from_csv('contacts.csv')
        elif choice == '0':
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()