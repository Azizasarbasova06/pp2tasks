#1
thislist = ["apple", "banana", "cherry"]
print(thislist)

#2(Return the third, fourth, and fifth item)

thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[2:5])

#3(Change the values "banana" and "cherry" with the values "blackcurrant" and "watermelon")

thislist = ["apple", "banana", "cherry", "orange", "kiwi", "mango"]
thislist[1:3] = ["blackcurrant", "watermelon"]
print(thislist)

#4(Insert an item as the second position)

thislist = ["apple", "banana", "cherry"]
thislist.insert(1, "orange")
print(thislist)

#5(Remove the first occurrence of "banana")

thislist = ["apple", "banana", "cherry", "banana", "kiwi"]
thislist.remove("banana")
print(thislist)

#6 (Print all items in the list, one by one)

thislist = ["apple", "banana", "cherry"]
for x in thislist:
  print(x)

#7 (Accept only numbers lower than 5)

newlist = [x for x in range(10) if x < 5]

#8 (Sort the list numerically)

thislist = [100, 50, 65, 82, 23]
thislist.sort()
print(thislist)

#9 (Make a copy of a list with the copy() method)

thislist = ["apple", "banana", "cherry"]
mylist = thislist.copy()
print(mylist)

#10 (Join two list)

list1 = ["a", "b", "c"]
list2 = [1, 2, 3]

list3 = list1 + list2
print(list3)
