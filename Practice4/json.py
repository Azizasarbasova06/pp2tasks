import json

# 1. Конвертация Python словаря в JSON строку (dumps)
person = {"name": "Aziza", "university": "KBTU", "skills": ["Python", "Git"]}
json_string = json.dumps(person, indent=4)
print("JSON String:", json_string)

# 2. Парсинг JSON строки в словарь (loads)
json_input = '{"course": "PP2", "semester": 2}'
data = json.loads(json_input)
print("Course name:", data["course"])

# 3. Запись данных в файл (dump)
with open('data.json', 'w') as f:
    json.dump(person, f)

# 4. Чтение из файла (например, sample-data.json)
# Раскомментируй это, когда файл будет в папке:
"""
with open('sample-data.json', 'r') as f:
    sample_data = json.load(f)
    print("Data from file:", sample_data)
"""