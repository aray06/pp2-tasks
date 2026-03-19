from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# Map: возведение в квадрат
squared = list(map(lambda x: x**2, numbers))

# Filter: только четные
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Reduce: сумма всех элементов
total_sum = reduce(lambda x, y: x + y, numbers)

print(f"Squared: {squared}\nEvens: {evens}\nSum: {total_sum}")