#1
def square_generator(N):
    for i in range(N + 1):
        yield i ** 2

N = 5
for square in square_generator(N):
    print(square, end=" ")  # Output: 0 1 4 9 16 25


#2
n = int(input("Enter n: "))

def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

print(",".join(str(num) for num in even_numbers(n)))

#3
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = 50
for num in divisible_by_3_and_4(n):
    print(num, end=" ")  # Output: 0 12 24 36 48

#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

for sq in squares(3, 7):
    print(sq)

#5
def countdown(n):
    for i in range(n, -1, -1):
        yield i

n = 5
for num in countdown(n):
    print(num, end=" ")  # Output: 5 4 3 2 1 0