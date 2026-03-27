#1
txt = "Hello Sam!"

mytable = str.maketrans("S", "P")

print(txt.translate(mytable))



#2
txt = "hello, and welcome to my world."

x = txt.capitalize()

print (x)


#3
txt = "banana"

x = txt.center(20)

print(x)


#4
txt = "Hello, welcome to my world."

x = txt.endswith(".")

print(x)


#5
txt = "CompanyX"

x = txt.isalpha()

print(x)