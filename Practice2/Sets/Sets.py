#1 (Check if "banana" is present in the set)

thisset = {"apple", "banana", "cherry"}

print("banana" in thisset)

#2 (Add elements from tropical into thisset)

thisset = {"apple", "banana", "cherry"}
tropical = {"pineapple", "mango", "papaya"}

thisset.update(tropical)

print(thisset)

#3 (Remove a random item by using the pop() method)

thisset = {"apple", "banana", "cherry"}

x = thisset.pop()

print(x)

print(thisset)

#4 (Loop through the set, and print the values)

thisset = {"apple", "banana", "cherry"}

for x in thisset:
  print(x)

#5 (Use | to join two sets)

set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

set3 = set1 | set2
print(set3)

#6 (Create a frozenset and check its type)

x = frozenset({"apple", "banana", "cherry"})
print(x)
print(type(x))

