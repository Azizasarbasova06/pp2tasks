import csv
import json
from datetime import datetime
from pathlib import Path

from psycopg2.extras import RealDictCursor
from connect import get_connection


VALID_PHONE_TYPES = {"home", "work", "mobile"}
VALID_SORT_FIELDS = {
    "name": "c.name",
    "birthday": "c.birthday",
    "date": "c.date_added",
    "date_added": "c.date_added",
}


def normalize_date(value):
    if value is None or str(value).strip() == "":
        return None
    value = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Invalid date '{value}'. Use YYYY-MM-DD.")


def get_or_create_group(cur, group_name):
    group_name = (group_name or "Other").strip() or "Other"
    cur.execute(
        """
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id
        """,
        (group_name,),
    )
    row = cur.fetchone()
    if row:
        return row[0] if not isinstance(row, dict) else row["id"]

    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    row = cur.fetchone()
    return row[0] if not isinstance(row, dict) else row["id"]


def find_contact_by_name(cur, name):
    cur.execute("SELECT id FROM contacts WHERE name = %s LIMIT 1", (name,))
    return cur.fetchone()


def create_contact(cur, name, email=None, birthday=None, group_name="Other"):
    group_id = get_or_create_group(cur, group_name)
    cur.execute(
        """
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """,
        (name, email, normalize_date(birthday), group_id),
    )
    row = cur.fetchone()
    return row[0] if not isinstance(row, dict) else row["id"]


def overwrite_contact(cur, contact_id, email=None, birthday=None, group_name="Other"):
    group_id = get_or_create_group(cur, group_name)
    cur.execute(
        """
        UPDATE contacts
        SET email = %s,
            birthday = %s,
            group_id = %s
        WHERE id = %s
        """,
        (email, normalize_date(birthday), group_id, contact_id),
    )
    cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))


def add_phone_local(cur, contact_id, phone, phone_type):
    phone = str(phone).strip()
    phone_type = (phone_type or "mobile").strip().lower()

    if not phone:
        return

    if phone_type not in VALID_PHONE_TYPES:
        raise ValueError(f"Invalid phone type '{phone_type}'. Use home, work, or mobile.")

    cur.execute(
        """
        INSERT INTO phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
        """,
        (contact_id, phone, phone_type),
    )


def add_phone_procedure():
    name = input("Contact name: ").strip()
    phone = input("Phone: ").strip()
    phone_type = input("Type [home/work/mobile]: ").strip().lower()

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
        conn.commit()
    print("Phone added.")


def move_to_group_procedure():
    name = input("Contact name: ").strip()
    group = input("New group: ").strip()

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
    print("Contact moved.")


def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    for row in rows:
        print("-" * 70)
        print(f"ID:       {row.get('contact_id') or row.get('id')}")
        print(f"Name:     {row.get('name')}")
        print(f"Email:    {row.get('email') or ''}")
        print(f"Birthday: {row.get('birthday') or ''}")
        print(f"Group:    {row.get('group_name') or ''}")
        print(f"Phones:   {row.get('phones') or ''}")
        if row.get("date_added"):
            print(f"Added:    {row.get('date_added')}")
    print("-" * 70)


def list_contacts(group=None, email_query=None, sort_by="name", limit=10, offset=0):
    sort_col = VALID_SORT_FIELDS.get(sort_by, "c.name")

    where = []
    params = []

    if group:
        where.append("g.name ILIKE %s")
        params.append(group)

    if email_query:
        where.append("c.email ILIKE %s")
        params.append(f"%{email_query}%")

    where_sql = "WHERE " + " AND ".join(where) if where else ""

    sql = f"""
        SELECT
            c.id AS contact_id,
            c.name,
            c.email,
            c.birthday,
            c.date_added,
            g.name AS group_name,
            COALESCE(
                string_agg(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.type, p.phone),
                ''
            ) AS phones
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        {where_sql}
        GROUP BY c.id, c.name, c.email, c.birthday, c.date_added, g.name
        ORDER BY {sort_col} NULLS LAST, c.name
        LIMIT %s OFFSET %s
    """
    params.extend([limit, offset])

    with get_connection(dict_cursor=True) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()


def advanced_search():
    query = input("Search name/email/group/phone: ").strip()

    with get_connection(dict_cursor=True) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            rows = cur.fetchall()

    print_contacts(rows)


def filter_sort_contacts():
    group = input("Group filter, empty for all: ").strip() or None
    email = input("Email partial search, empty for all: ").strip() or None
    sort_by = input("Sort by [name/birthday/date]: ").strip().lower() or "name"

    if sort_by not in VALID_SORT_FIELDS:
        print("Invalid sort field. Using name.")
        sort_by = "name"

    rows = list_contacts(group=group, email_query=email, sort_by=sort_by)
    print_contacts(rows)


def paginated_navigation():
    """
    Console pagination loop.
    This uses the already-existing pagination function if it is named get_contacts_paginated(limit, offset).
    If your Practice 8 function has another name, update the SELECT line below.
    """
    page_size_raw = input("Page size [5]: ").strip()
    page_size = int(page_size_raw) if page_size_raw else 5
    page = 0

    while True:
        offset = page * page_size

        with get_connection(dict_cursor=True) as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        "SELECT * FROM get_contacts_paginated(%s, %s)",
                        (page_size, offset),
                    )
                    rows = cur.fetchall()
                except Exception:
                    conn.rollback()
                    rows = list_contacts(limit=page_size, offset=offset)

        print(f"\nPage {page + 1}")
        print_contacts(rows)

        command = input("[next / prev / quit]: ").strip().lower()
        if command in {"q", "quit", "exit"}:
            break
        if command in {"n", "next"}:
            page += 1
        elif command in {"p", "prev"}:
            page = max(0, page - 1)


def export_to_json(path="contacts.json"):
    sql = """
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            c.date_added,
            g.name AS group_name,
            COALESCE(
                json_agg(
                    json_build_object('phone', p.phone, 'type', p.type)
                    ORDER BY p.type, p.phone
                ) FILTER (WHERE p.id IS NOT NULL),
                '[]'
            ) AS phones
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        GROUP BY c.id, c.name, c.email, c.birthday, c.date_added, g.name
        ORDER BY c.name
    """

    with get_connection(dict_cursor=True) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

    data = []
    for row in rows:
        item = dict(row)
        if item.get("birthday"):
            item["birthday"] = item["birthday"].isoformat()
        if item.get("date_added"):
            item["date_added"] = item["date_added"].isoformat()
        data.append(item)

    Path(path).write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")
    print(f"Exported {len(data)} contacts to {path}.")


def import_from_json(path="contacts.json"):
    data = json.loads(Path(path).read_text(encoding="utf-8"))

    with get_connection() as conn:
        with conn.cursor() as cur:
            for item in data:
                name = str(item["name"]).strip()
                email = item.get("email")
                birthday = item.get("birthday")
                group_name = item.get("group_name") or item.get("group") or "Other"
                phones = item.get("phones") or []

                existing = find_contact_by_name(cur, name)
                if existing:
                    contact_id = existing[0]
                    decision = input(f'Duplicate "{name}". skip or overwrite? [s/o]: ').strip().lower()
                    if decision not in {"o", "overwrite"}:
                        print(f"Skipped {name}.")
                        continue
                    overwrite_contact(cur, contact_id, email, birthday, group_name)
                else:
                    contact_id = create_contact(cur, name, email, birthday, group_name)

                for phone_obj in phones:
                    if isinstance(phone_obj, dict):
                        phone = phone_obj.get("phone")
                        phone_type = phone_obj.get("type", "mobile")
                    else:
                        phone = phone_obj
                        phone_type = "mobile"
                    add_phone_local(cur, contact_id, phone, phone_type)

        conn.commit()

    print("JSON import complete.")


def import_from_csv(path="contacts.csv"):
    """
    Expected CSV columns:
    name,email,birthday,group,phone,type

    Multiple rows with the same name can be used for multiple phone numbers.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    name = row["name"].strip()
                    email = row.get("email")
                    birthday = row.get("birthday")
                    group_name = row.get("group") or row.get("group_name") or "Other"
                    phone = row.get("phone")
                    phone_type = row.get("type") or row.get("phone_type") or "mobile"

                    existing = find_contact_by_name(cur, name)
                    if existing:
                        contact_id = existing[0]
                        cur.execute(
                            """
                            UPDATE contacts
                            SET email = COALESCE(%s, email),
                                birthday = COALESCE(%s, birthday),
                                group_id = %s
                            WHERE id = %s
                            """,
                            (
                                email,
                                normalize_date(birthday),
                                get_or_create_group(cur, group_name),
                                contact_id,
                            ),
                        )
                    else:
                        contact_id = create_contact(cur, name, email, birthday, group_name)

                    add_phone_local(cur, contact_id, phone, phone_type)

        conn.commit()

    print("CSV import complete.")


def add_contact_console():
    name = input("Name: ").strip()
    email = input("Email: ").strip() or None
    birthday = input("Birthday YYYY-MM-DD: ").strip() or None
    group_name = input("Group [Family/Work/Friend/Other]: ").strip() or "Other"

    phones = []
    while True:
        phone = input("Phone, empty to stop: ").strip()
        if not phone:
            break
        phone_type = input("Type [home/work/mobile]: ").strip().lower() or "mobile"
        phones.append((phone, phone_type))

    with get_connection() as conn:
        with conn.cursor() as cur:
            contact_id = create_contact(cur, name, email, birthday, group_name)
            for phone, phone_type in phones:
                add_phone_local(cur, contact_id, phone, phone_type)
        conn.commit()

    print("Contact added.")


def menu():
    while True:
        print("""
Extended PhoneBook
1. Add contact with extended fields
2. Filter/search/sort contacts
3. Advanced search across name, email, group, phones
4. Paginated navigation
5. Export to JSON
6. Import from JSON
7. Import from CSV
8. Add phone using procedure
9. Move contact to group using procedure
0. Exit
""")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                add_contact_console()
            elif choice == "2":
                filter_sort_contacts()
            elif choice == "3":
                advanced_search()
            elif choice == "4":
                paginated_navigation()
            elif choice == "5":
                path = input("Output JSON path [contacts.json]: ").strip() or "contacts.json"
                export_to_json(path)
            elif choice == "6":
                path = input("Input JSON path [contacts.json]: ").strip() or "contacts.json"
                import_from_json(path)
            elif choice == "7":
                path = input("Input CSV path [contacts.csv]: ").strip() or "contacts.csv"
                import_from_csv(path)
            elif choice == "8":
                add_phone_procedure()
            elif choice == "9":
                move_to_group_procedure()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
        except Exception as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    menu()
