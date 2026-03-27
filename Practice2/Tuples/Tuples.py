#1 (Create a Tuple)

thistuple = ("apple", "banana", "cherry")
print(thistuple)

#2 (Print the last item of the tuple)

thistuple = ("apple", "banana", "cherry")
print(thistuple[-1])

#3 (Convert the tuple into a list to be able to change it)

x = ("apple", "banana", "cherry")
y = list(x)
y[1] = "kiwi"
x = tuple(y)

print(x)

#4 (Unpacking a tuple)

fruits = ("apple", "banana", "cherry")

(green, yellow, red) = fruits

print(green)
print(yellow)
print(red)

#5 (Iterate through the items and print the values)

thistuple = ("apple", "banana", "cherry")
for x in thistuple:
  print(x)

#6(Join two tuples)

tuple1 = ("a", "b" , "c")
tuple2 = (1, 2, 3)

tuple3 = tuple1 + tuple2
print(tuple3)