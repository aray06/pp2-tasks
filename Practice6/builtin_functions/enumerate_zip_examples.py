names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 95]

# Enumerate: индекс и значение
for index, name in enumerate(names):
    print(f"{index}: {name}")

# Zip: объединение списков
for name, score in zip(names, scores):
    print(f"{name} scored {score}")