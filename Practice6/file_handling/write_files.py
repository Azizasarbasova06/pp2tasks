# Создаём и записываем файл

# "w"- создаёт файл или перезаписывает его
with open("example.txt", "w") as f:
    f.write("Hello\n")
    f.write("This is Practice 6\n")
print("Файл создан и записан (режим w)")

# "a" - добавляет текст в конец файла
with open("example.txt", "a") as f:
    f.write("New line added\n")
print("Добавлена новая строка (режим a)")

# "x" - создаёт новый файл, если его нет
try:
    with open("new_file.txt", "x") as f:
        f.write("Created with x mode")
    print("Файл создан (режим x)")
except FileExistsError:
    print("Файл уже существует (x не сработал)")