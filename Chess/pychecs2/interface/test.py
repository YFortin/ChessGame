annee = input()
try:
    annee = int(annee)

if annee <= 0:
    raise ValueError("l’année entrée est <= 0")

except ValueError as e:
    print("Exception: {}", e)