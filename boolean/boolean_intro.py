#1 example
a = 200
b = 33

if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

#2 example
print(bool("Hello"))
print(bool(15))

#3 example
x = "Hello"
y = 15

print(bool(x))
print(bool(y))

#4 example
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

#5 example
class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))