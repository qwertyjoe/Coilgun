import math

V = float(input("Input V0: "))
g = float(input("Input g: "))
x = int(input("Input x: "))
y = int(input("Input y: "))

V_Pow_2 = math.pow(V,2)
V_Pow_4 = math.pow(V,4)
G_Pow_2 = math.pow(g,2)
X_Pow_2 = math.pow(x,2)

Sqrt_ans = math.sqrt(V_Pow_4-2*g*V_Pow_2*y-G_Pow_2*X_Pow_2) / (g*x)

Up = ( V_Pow_2 / (g*x) ) + (Sqrt_ans)
Down = ( V_Pow_2 / (g*x) ) - (Sqrt_ans)

print("addition radians:",math.atan(Up))
print("subtraction radians:",math.atan(Down))

print("addition degrees:",math.degrees(math.atan(Up)))
print("subtraction degrees:",math.degrees(math.atan(Down)))

