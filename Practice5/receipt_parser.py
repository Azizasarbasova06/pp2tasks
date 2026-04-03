import re
import json

# УПРАЖНЕНИЯ ПО REGEX

# 1. 'a', за которой следует ноль или более 'b'. * — квантификатор "0 или больше"
def task1(text): return re.fullmatch(r"ab*", text)

# 2. 'a', за которой следуют от 2 до 3 'b'. {2,3} — задает точный диапазон
def task2(text): return re.fullmatch(r"ab{2,3}", text)

# 3. Строчные буквы, соединенные подчеркиванием (hello_world)
def task3(text): return re.findall(r"[a-z]+_[a-z]+", text)

# 4. Одна заглавная буква, за которой следуют только строчные
def task4(text): return re.findall(r"[A-Z][a-z]+", text)

# 5. 'a' за которой следует любой текст, и всё это заканчивается на 'b'
def task5(text): return re.fullmatch(r"a.*b", text)

# 6. Замена пробела, запятой или точки на двоеточие через re.sub
def task6(text): return re.sub(r"[ ,.]", ":", text)

# 7. Конвертация snake_case (с нижним подчеркиванием) в camelCase
def task7(text): 
    words = text.split('_')
    return words[0] + ''.join(w.capitalize() for w in words[1:])

# 8. Разбить строку там, где стоят заглавные буквы не удаляя их
def task8(text): return re.split(r"(?=[A-Z])", text)

# 9. Вставить пробелы между словами которые начинаются с заглавной буквы
def task9(text): return re.sub(r"(\w)([A-Z])", r"\1 \2", text)

# 10. Конвертация camelCase обратно в snake_case.
# Используются группы ( ) и обратные ссылки \1, \2 для вставки подчеркивания
def task10(text):
    res = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', res).lower()


# ПАРСИНГ ЧЕКa

def parse_europharma_receipt(file_name):
    try:
        # Открываем файл с кодировкой utf-8, чтобы правильно читалась кириллица
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. ПОИСК ДАТЫ И ВРЕМЕНИ
        # \d{2} означает две цифры. Ищем формат ДД.ММ.ГГГГ и ЧЧ:ММ:СС
        date_match = re.search(r"(\d{2}\.\d{2}\.\d{4})", content)
        time_match = re.search(r"(\d{2}:\d{2}:\d{2})", content)

        # 2. ПОИСК ИТОГОВОЙ СУММЫ
        # [\d\s]+ позволяет захватить цифры вместе с пробелами (например, "18 009")
        total_match = re.search(r"ИТОГО:\s*([\d\s]+,\d{2})", content)
        # Очищаем данные: убираем пробелы и меняем запятую на точку для формата числа
        total_val = total_match.group(1).replace(" ", "").replace(",", ".") if total_match else "0.00"

        # 3. ПОИСК НАЗВАНИЙ ТОВАРОВ
        # Используем флаг re.DOTALL, чтобы точка . ловила и переносы строк
        # Ищем текст между номером (1) и строкой с количеством (x).
        products = re.findall(r"\d+\.\n(.*?)(?=\s+\d+,\d{3}\s+x)", content, re.DOTALL)

        # 4. ПОИСК ЦЕН ТОВАРОВ
        # Вытаскиваем все значения, которые стоят после слова "Стоимость"
        item_prices = re.findall(r"Стоимость\s+([\d\s]+,\d{2})", content)
        clean_prices = [p.replace(" ", "").replace(",", ".") for p in item_prices]

        # 5. СПОСОБ ОПЛАТЫ
        # re.IGNORECASE позволяет не зависеть от регистра букв
        payment = re.search(r"(Банковская карта|Наличные)", content, re.IGNORECASE)

        # Формируем итоговый словарь 
        return {
            "store": "EUROPHARMA Astana",
            "date": date_match.group(1) if date_match else "None",
            "time": time_match.group(1) if time_match else "None",
            "items": [
                {"name": name.strip().replace("\n", " "), "price": price} 
                for name, price in zip(products, clean_prices)
            ],
            "total_amount": total_val,
            "payment_method": payment.group(0) if payment else "Unknown"
        }

    except FileNotFoundError:
        return "Ошибка: Файл raw.txt не найден в папке Practice5!"


# ЗАПУСК И ТЕСТИРОВАНИЕ
if __name__ == "__main__":
    
    # Задание 1: 'a' + ноль или более 'b'
    print(f"Task 1 (abb): {bool(task1('abb'))}")
    
    # Задание 2: 'a' + от 2 до 3 'b'
    print(f"Task 2 (abbb): {bool(task2('ab'))}")
    
    # Задание 3: Строчные буквы с подчеркиванием
    print(f"Task 3: {task3('find hello_world and test_case')}")
    
    # Задание 4: Заглавная + строчные
    print(f"Task 4: {task4('Aziza Kbtu python')}")
    
    # Задание 5: 'a' + что угодно + 'b' в конце
    print(f"Task 5 (axxxb): {bool(task5('axxxbc'))}")
    
    # Задание 6: Замена пробела/запятой/точки на :
    print(f"Task 6: {task6('Python, Exercises. at KBTU')}")
    
    # Задание 7: snake_case -> camelCase
    print(f"Task 7: {task7('my_secret_variable')}")
    
    # Задание 8: Разрыв по заглавным буквам
    print(f"Task 8: {task8('SplitAtUppercase')}")
    
    # Задание 9: Пробелы между словами с большой буквы
    print(f"Task 9: {task9('InsertSpacesHere')}")
    
    # Задание 10: camelCase -> snake_case
    print(f"Task 10: {task10('EuroPharmaApp')}")

    print("\n" + "="*40)
    # Запускаем парсинг чека
    print("--- РЕЗУЛЬТАТ ПАРСИНГА ЧЕКА EUROPHARMA ---")
    data = parse_europharma_receipt('raw.txt')
    print(json.dumps(data, indent=4, ensure_ascii=False))