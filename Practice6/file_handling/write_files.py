# Режимы 'w' (перезапись) и 'a' (добавление)
with open("output.txt", "w") as f:
    f.write("Initial content.\n")

with open("output.txt", "a") as f:
    f.write("Appended line.\n")