#A function with one argument:
def my_function(fname):
  print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus")


#This function expects 2 arguments, and gets 2 arguments::
def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Emil", "Refsnes")


#Default value for country parameter:
def my_function(country = "Norway"):
  print("I am from", country)

my_function("Sweden")
my_function("India")
my_function()
my_function("Brazil")