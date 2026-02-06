#1 (Print only odd numbers by skipping the even ones)

for i in range(1, 6):
    if i % 2 == 0:
        continue
    print(i)  # Output: 1, 3, 5

#2 (Print all fruits except "banana")

fruits = ["apple", "banana", "cherry"]
for f in fruits:
    if f == "banana":
        continue
    print(f)

#3 (Process only positive numbers from a list)

prices = [10, -5, 20, -1, 30]
for p in prices:
    if p < 0:
        continue
    print("Price:", p)

#4 (Print a string but remove all spaces)

text = "Hello World"
for char in text:
    if char == " ":
        continue
    print(char, end="")

#5 (Process items but skip the one labeled "empty")

data = ["valid", "empty", "valid", "valid"]
for item in data:
    if item == "empty":
        continue
    print("Processing:", item) 