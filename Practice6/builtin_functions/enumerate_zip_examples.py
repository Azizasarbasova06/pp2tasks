# enumerate() и zip()

names = ["Ali", "Aruzhan", "Dana"]
scores = [90, 85, 88]

# enumerate() - даёт индекс и значение
print("enumerate:")
for i, name in enumerate(names):
    print(i, name)

# zip() - объединяет два списка
print("zip:")
for name, score in zip(names, scores):
    print(name, score)

# sorted() - сортировка
print("sorted scores:")
print(sorted(scores))