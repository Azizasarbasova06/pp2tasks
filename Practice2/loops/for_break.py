#1 (End the loop if i is larger than 3)

for i in range(9):
  if i > 3:
    break
  print(i)

#2 (Stop looking once you find the number 5)

for i in range(1, 10):
    if i == 5:
        break
    print(i)

#3 (Stop the loop if the word "Stop" appears in the list)

words = ["Go", "Run", "Stop", "Jump"]
for w in words:
    if w == "Stop":
        break
    print(w)

#4 (Print a name until you hit a specific letter)

for letter in "Python":
    if letter == "h":
        break
    print(letter)

#5 (Exit the loop after printing the first 3 items0

for i in range(100):
    if i == 3:
        break
    print("Item", i)