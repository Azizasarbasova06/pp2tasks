#1 (Exit the loop when i is 3)

i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1

#2 (Remove and print items from a list until it is empty)

tasks = ["Email", "Call", "Code"]
while tasks:
    current = tasks.pop()
    print("Doing task:", current)

#3 (Continue to the next iteration if i is 3)

i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)

#4 (Print a message once the condition is false)

i = 1
while i < 6:
  print(i)
  i += 1
else:
  print("i is no longer less than 6")
  
#5 (Double a number until it exceeds 100)

num = 1
while num <= 100:
    print(num)
    num *= 2