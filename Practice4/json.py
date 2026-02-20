import json

# 1. Открываем и загружаем JSON файл
with open('sample-data.json', 'r') as file:
    data = json.load(file)

# 2. Печатаем заголовок таблицы (точно как в задании)
print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<8} {'MTU':<6}")
print(f"{'-' * 50} {'-' * 20} {'-' * 6} {'-' * 6}")

# 3. Проходим циклом по списку интерфейсов в imdata
for item in data["imdata"]:
    # Извлекаем атрибуты из вложенного словаря
    attr = item["l1PhysIf"]["attributes"]
    
    dn = attr["dn"]
    description = attr["descr"]
    speed = attr["speed"]
    mtu = attr["mtu"]
    
    # Печатаем строку таблицы с выравниванием
    # <50 значит "занять 50 символов и выровнять по левому краю"
    print(f"{dn:<50} {description:<20} {speed:<8} {mtu:<6}")