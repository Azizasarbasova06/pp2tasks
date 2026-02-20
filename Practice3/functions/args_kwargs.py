# 1. *args для суммирования всех трат
def total_expenses(*amounts):
    total = sum(amounts)
    print(f"Общая сумма расходов: {total} KZT")
    return total

# 2. **kwargs для детальной информации о товаре
def product_details(name, **features):
    print(f"Детали товара '{name}':")
    for key, value in features.items():
        print(f"- {key}: {value}")

# 3. Обязательные аргументы + *args
def print_student_list(group_id, *students):
    print(f"Группа {group_id}: {', '.join(students)}")

# 4. Полная комбинация
def system_log(level, *messages, **meta):
    print(f"[{level.upper()}] {' | '.join(messages)}")
    print(f"Metadata: {meta}")

product_details("Медовик", weight="1.5kg", organic=True, rating=5.0)