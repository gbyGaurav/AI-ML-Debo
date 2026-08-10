
''' Day 1: Python Fundamentals
   Name: Gaurav Bharat Deore
   Contact no : 9373446328
   Email :bharatdeore7813@gmail.com
   Description : Topics that are covered on day 1
   Topics : 1) virtual environment ,2) vscode/jupyter notebook/kaggle ,3) commands ,4) DataTypes, 5) dictionary, 6) List , 
   7) Indexing, 8) Slicing , 9)Conditional Statements, 10)For loop, 11) While loop'''

# DataTypes
x = int(input('Enter a random number:'))
print(type(x))

# string to int
x ='12'
print(int(x))

# dictionary
dict = {'x':'gaurav', 'y':'aditya','z':'sakshiee'}
print(dict['y'])

# list
list = [2,'gaurav',3.14,True,dict]
print(list)

# indexing
print(list[3])  #+ve indexing
print(list[-2]) #-ve indexing

# slicing
print(list[1:3])

# question1 : take an string
str = 'my name is Gaurav, im from sapkal'

#question 2: print char upto index 6
print(str[0:6])

#question 3: print strings by removing first 2 chars
print(str[2:])

#question 4 : print middle char from str
print(str[11:17])

# formulate an problem statement based on conditional statement
marks = int(input('Enter your marks:'))

if marks <= 80 :
  print("Grade C")
elif marks > 80 and marks <= 90:
  print("Grade B")
else:
  print("Grade A")

"""Homework
"""

# formulate an problem statement on for loop
# Example 1
for i in range(1,11):
  print(i)

# Example 2
for i in range(0,21,2):
  print(i)

# formulate an problem wih while loop
# Example 1|
n = int(input("Enter an number:"))
i = 1
while i <=10:
  print(i * n)
  i += 1

# Example 2
list = [5,10,15,20,25,30,35,40,45,50]
num = int(input("Enter number to find:"))
i = 0
while i < len(list):
  if list[i] == num:
    print('Number found at', i)
  i += 1

