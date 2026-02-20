import math

# --- Task 1: Degree to Radian ---
# Formula: Radian = Degree * (pi / 180)
degree = float(input("Input degree: "))
radian = math.radians(degree)
print(f"Output radian: {radian:.6f}")

print("-" * 30)

# --- Task 2: Area of a trapezoid ---
# Formula: Area = ((a + b) / 2) * h
height_trap = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
area_trap = ((base1 + base2) / 2) * height_trap
print(f"Expected Output: {area_trap}")

print("-" * 30)

# --- Task 3: Area of regular polygon ---
# Formula: Area = (n * s^2) / (4 * tan(pi / n))

n_sides = int(input("Input number of sides: "))
side_len = float(input("Input the length of a side: "))
area_poly = (n_sides * side_len**2) / (4 * math.tan(math.pi / n_sides))
print(f"The area of the polygon is: {area_poly:.0f}")

print("-" * 30)

# --- Task 4: Area of a parallelogram ---
# Formula: Area = base * height
base_par = float(input("Length of base: "))
height_par = float(input("Height of parallelogram: "))
area_par = base_par * height_par
print(f"Expected Output: {area_par:.1f}")