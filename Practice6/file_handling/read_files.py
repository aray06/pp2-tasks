# Чтение всего файла, одной строки и списка строк
with open("test.txt", "w") as f:
    f.write("Hello KBTU!\nThis is Practice 6.\nPython is great.")

with open("test.txt", "r") as f:
    print("Full Read:\n", f.read())

with open("test.txt", "r") as f:
    f.seek(0)
    print("Readlines:", f.readlines())