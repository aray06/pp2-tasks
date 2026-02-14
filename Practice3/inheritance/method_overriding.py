#Method overriding — это когда дочерний класс переопределяет метод родительского класса.
class Person:
    def speak(self):
        print("I am a person")

class Student(Person):
    def speak(self):   # ← overriding
        print("I am a student")
