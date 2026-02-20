import json

# Загружаем данные из файла
with open('sample-data.json', 'r') as f:
    data = json.load(f)

# Печатаем шапку таблицы
print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<8} {'MTU':<6}")
print(f"{'-' * 50} {'-' * 20} {'-' * 6} {'-' * 6}")

# Проходим по элементам imdata
for item in data["imdata"]:
    attr = item["l1PhysIf"]["attributes"]
    dn = attr["dn"]
    descr = attr["descr"] if attr["descr"] else ""
    speed = attr["speed"]
    mtu = attr["mtu"]
    
    # Форматированный вывод строки
    print(f"{dn:<50} {descr:<20} {speed:<8} {mtu:<6}")