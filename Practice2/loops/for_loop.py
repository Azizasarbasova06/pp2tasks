#1 (Print each number from 1 to 8)

for x in range(1, 9):
  print(x)

#2 (Loop through all items in a list)

fruits = ["apple", "banana", "cherry"]

for x in fruits:
  print(x)

#3 (Calculate the total of several numbers)

numbers = [10, 20, 30]
total = 0
for n in numbers:
    total += n
print("Total:", total)

#4 (Print the item along with its position (index))

colors = ["Red", "Green", "Blue"]
for index, color in enumerate(colors):
    print(f"{index}: {color}")

#5 (Print every item in a shopping list)

items = ["Milk", "Bread", "Eggs"]
for item in items:
    print("Buy:", item)