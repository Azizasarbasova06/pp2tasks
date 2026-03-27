#1
print(10 > 9)
print(10 == 9)
print(10 < 9)

#2
a = 200
b = 33

if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

#3
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

#4
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})

#5
def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!")