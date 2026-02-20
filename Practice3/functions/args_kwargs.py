# *args для кортежа аргументов, **kwargs для словаря
def print_everything(*args, **kwargs):
    print("Positional:", args)
    print("Keyword:", kwargs)

print_everything(1, 2, 3, course="PP2", university="KBTU")