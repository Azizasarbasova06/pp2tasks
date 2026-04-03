from connect import connect


def добавить_или_обновить_пользователя():
    имя = input("Введите имя: ")
    фамилия = input("Введите фамилию: ")
    телефон = input("Введите телефон: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "CALL insert_or_update_user(%s, %s, %s);",
        (имя, фамилия, телефон)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Пользователь добавлен или обновлен")


def поиск_по_шаблону():
    шаблон = input("Введите текст для поиска: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_by_pattern(%s);", (шаблон,))
    rows = cur.fetchall()

    print("\nРезультаты поиска:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def показать_с_пагинацией():
    limit = int(input("Введите LIMIT: "))
    offset = int(input("Введите OFFSET: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s, %s);",
        (limit, offset)
    )

    rows = cur.fetchall()

    print("\nРезультаты:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def удалить_пользователя():
    значение = input("Введите имя или телефон для удаления: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_user(%s);", (значение,))
    conn.commit()

    cur.close()
    conn.close()

    print("Пользователь удален")


def добавить_несколько():
    количество = int(input("Сколько пользователей добавить: "))

    имена = []
    фамилии = []
    телефоны = []

    for _ in range(количество):
        имя = input("Имя: ")
        фамилия = input("Фамилия: ")
        телефон = input("Телефон: ")

        имена.append(имя)
        фамилии.append(фамилия)
        телефоны.append(телефон)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "CALL insert_many_users(%s, %s, %s);",
        (имена, фамилии, телефоны)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Массовое добавление завершено")


def меню():
    while True:
        print("\n--- ТЕЛЕФОННАЯ КНИГА ---")
        print("1. Добавить или обновить пользователя")
        print("2. Поиск")
        print("3. Добавить несколько пользователей")
        print("4. Показать с пагинацией")
        print("5. Удалить пользователя")
        print("6. Выход")

        выбор = input("Выберите действие: ")

        if выбор == "1":
            добавить_или_обновить_пользователя()

        elif выбор == "2":
            поиск_по_шаблону()

        elif выбор == "3":
            добавить_несколько()

        elif выбор == "4":
            показать_с_пагинацией()

        elif выбор == "5":
            удалить_пользователя()

        elif выбор == "6":
            print("Выход...")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    меню()