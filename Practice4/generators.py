# 1. Создание и использование итератора (iter, next)
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)
print(next(myit))
print(next(myit))

# 2. Функция-генератор с yield (Генератор квадратов)
def square_generator(n):
    for i in range(n):
        yield i ** 2

for val in square_generator(5):
    print(val)

# 3. Выражение-генератор (Generator Expression)
even_gen = (x for x in range(10) if x % 2 == 0)
print(list(even_gen))

# 4. Пользовательский итератор (Класс с __iter__ и __next__)
class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self
    def __next__(self):
        if self.a <= 5:
            x = self.a
            self.a += 1
            return x
        else:
            raise StopIteration

myclass = MyNumbers()
for x in iter(myclass):
    print(x)