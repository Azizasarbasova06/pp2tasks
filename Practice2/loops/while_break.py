#1 Break out of a while loop:

i = 1
while i < 9:
  print(i)
  if i == 3:
    break
  i += 1

#2 (Keep asking for words until the user types "stop")

while True:
    word = input("Enter a word: ")
    if word == "stop":
        break
    print("You typed:", word)

#3 (Stop the loop when the correct number is guessed)

secret = 7
while True:
    guess = int(input("Guess the number: "))
    if guess == secret:
        print("Correct!")
        break

#4 (Simulate checking a value and stopping when it hits a target)

value = 1
while value < 100:
    if value == 10:
        break
    print("Value is:", value)
    value += 1

#5 (Run a process until the battery percentage drops too low)

battery = 100
while battery > 0:
    if battery < 20:
        print("Low battery! Shutting down.")
        break
    print(f"Running... {battery}%")
    battery -= 10