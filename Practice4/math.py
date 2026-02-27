import math  
# Import the library for working with mathematical functions (pi, tan, radians)

# 1: CONVERT DEGREE TO RADIAN
# 180 degrees is exactly Pi radians.
# Get input and convert it to float
degree = float(input("Input degree: ")) 

# Convert using the formula: degrees * (Pi / 180). 
# We use math.pi for maximum precision.
radian = degree * (math.pi / 180)

# Output the result. 
# :.6f is formatting: keep exactly 6 decimal places.
print(f"Output radian: {radian:.6f}")

print("-" * 30)

# 2: AREA OF A TRAPEZOID
# To find the area, take the average value of the bases and multiply by the height.
# Request the height (h) and two bases (a and b)
height_trap = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

# Apply the formula: Area = ((a + b) / 2) * h
area_trap = ((base1 + base2) / 2) * height_trap

print(f"Expected Output: {area_trap}")

print("-" * 30)

# 3: AREA OF REGULAR POLYGON
# The area depends on the number of sides (n) and their length (s).
# n is the integer number of sides (int), s is the length (float)
n_sides = int(input("Input number of sides: "))
side_len = float(input("Input the length of a side: "))

# Use the trigonometric formula:
# Area = (n * s^2) / (4 * tan(pi / n))
# math.tan() calculates the tangent. The angle inside (pi / n) is in radians.
area_poly = (n_sides * side_len**2) / (4 * math.tan(math.pi / n_sides))

# Round to the nearest whole number (:.0f)
print(f"The area of the polygon is: {area_poly:.0f}")

print("-" * 30)

# 4: AREA OF A PARALLELOGRAM
# Get the base length and the height
base_par = float(input("Length of base: "))
height_par = float(input("Height of parallelogram: "))

# Formula: Area = base * height
area_par = base_par * height_par

# Output with one decimal place (:.1f) -> 30.0
print(f"Expected Output: {area_par:.1f}")