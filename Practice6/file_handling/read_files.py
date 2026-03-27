# read() - читает весь файл
with open("example.txt", "r") as f:
    content = f.read()
print("read():")
print(content)

# readline() - читает одну строку
with open("example.txt", "r") as f:
    line = f.readline()
print("readline():")
print(line)

# readlines() - читает все строки в список
with open("example.txt", "r") as f:
    lines = f.readlines()
print("readlines():")
print(lines)