#1 (Use the continue keyword in a while loop)

i = 0
while i < 9:
  i += 1
  if i == 3:
    continue
  print(i)

#2 (Print all users except the "admin")

users = ["Alice", "Admin", "Bob"]
index = -1
while index < len(users) - 1:
    index += 1
    if users[index] == "Admin":
        continue
    print("User:", users[index])

#3 (Process only positive numbers. Skip negative ones)

num = 10
while num > 0:
    num -= 1
    if num % 2 != 0: # If odd
        continue
    print("Even number:", num)

#4 (Ask for a password; if it’s too short, skip the "Success" message and ask again)

while True:
    pw = input("Create password: ")
    if len(pw) < 5:
        print("Too short!")
        continue
    print("Password accepted.")
    break

#5 (In a game, only let the player score on odd-numbered turns)

turn = 0
while turn < 6:
    turn += 1
    if turn % 2 == 0:
        continue
    print(f"Turn {turn}: You gained points!")