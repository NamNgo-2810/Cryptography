import random

p = int(input("Enter p: "))
g = int(input("Enter g: "))
a = random.randint(1, 100)
b = random.randint(1, 100)
A = ((pow(g, a)) % p)
B = ((pow(g, b)) % p)
Ka = ((pow(B, a)) % p)
Kb = ((pow(A, b)) % p)

print("Secret key at A = ", str(Ka))
print("Secret key at B = ", str(Kb))