#1
sum1 = 100 + 50      # 150 (100 + 50)
sum2 = sum1 + 250    # 400 (150 + 250)
sum3 = sum2 + sum2   # 800 (400 + 400)

#2(Arithmetic Operators)
x = 15
y = 4

print(x + y)
print(x - y)
print(x * y)
print(x / y)
print(x % y)
print(x ** y)
print(x // y)

#3(Assignment Operators)
numbers = [1, 2, 3, 4, 5]

if (count := len(numbers)) > 3:
    print(f"List has {count} elements")

#4(Logical Operators)
x = 5

print(x < 5 or x > 10)
 
#5(Identity Operators)
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x

print(x is z)
print(x is y)
print(x == y) 

#6(Membership Operators)
fruits = ["apple", "banana", "cherry"]

print("banana" in fruits)

#7(Bitwise Operators)
print(6 | 3)

#8(Precedence Operator)
print((6 + 3) - (6 + 3))