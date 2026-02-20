# filter() отбирает элементы по условию
nums = [1, 5, 8, 10, 13]
even_nums = list(filter(lambda x: x % 2 == 0, nums))
print(even_nums) # [8, 10]