''' Day 4: Python Fundamentals
   Date : 12 -Aug -2026
   Name: Gaurav Bharat Deore
   Contact no : 9373446328
   Email :bharatdeore7813@gmail.com
   Description : Topics that are covered on day 2
   Topics : 1) Defining Function,2) calling function ,3) None ,4)  Local scope , 5) Global scope , 
   7)Exception handling, 8) Minor project'''



# Functions and Error Handling

'''1) creating function
  - a reusable block of code , written once and run as many times as you like '''


def hello():
  print('Hey')
  print('Hey')
  print('Hey')
hello()
hello()
print('One more time')
hello()

a = int(input("enter a:"))
b =int(input("enter b:"))

def cal(a,b):
  sum = a + b
  print(sum)

cal(a,b) # parameter madhe arguments store hotat a,b = parameter ahet

# jevha func call karto tevha te astat parameters
# jevha func define krto toh arguments astat

a = int(input("enter a:"))
b = int(input("enter b:"))

def cal(a,b): # defining a function
  print(a % 2 == 0)
  print(a / b)
  print(a // b)

cal(a,b)  # calling a function

a = int(input("enter a:"))
b = int(input("enter b:"))

def add(a,b):
  return a + b
add(a,b)

import random
def get_answer(n):
  if n == 1:
    return "it is certain"
  elif n ==2:
    return "ask again later"
r = random.randint(1,9)
print(get_answer(r))

# None

spam = None
print(spam)

# Local scope - varaible access only inside the function

def spam():
  eggs ='hi'
print(eggs)  # bcz we are trying to access the local variable outside the function

# Global scope - variable globally access kru shakto

eggs = 'global value'

def spam():
  print(eggs)
spam()

eggs ='global' # global variable
def spam():
  eggs ='local' # local variable only access inside the spam
  print(eggs)

spam()
print(eggs)

# Exception handling

42/0

# try/ except - the mechanism

# exception handling - if we dont want to stop the execution of code in middle we use exception handling to overcome from that condition

a = int(input("enter a:"))
b = int(input("enter b:"))

def div(a,b):
  try:
    print(a/b)

  except:
    if a == 0 or b ==0:
      print("Division by zero error , enter no except 0")

div(a,b)

def spam(div):
  try:
    return 42 / div
  except ZeroDivisionError:
    print("Error: Invalid argument")

print(spam(2))
print(spam(12))
print(spam(0))
print(spam(3))

# Errors
# ZeroDivisionError 42/0 , ValueError int('abc) , TypeError '2'+2 , IndexError [1,2][5]

# hw 4 diff codes for this exceptions
