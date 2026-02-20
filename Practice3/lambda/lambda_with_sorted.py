# sorted() с ключом в виде лямбды
students = [("Ali", 20), ("Sanzhar", 18), ("Baur", 22)]
# Сортировка по возрасту (второй элемент кортежа)
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)