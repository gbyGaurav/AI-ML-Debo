# -*- coding: utf-8 -*-
"""
Date : 17- aug-2026
Description : Python Assignment
"""


# Question 1
nums = [12, 7, 9, 4, 22, 15, 8, 3, 30, 11]

even_cnt = 0
odd_cnt = 0

for num in nums:
    if num % 2 == 0:
        even_cnt += 1
    else:
        odd_cnt += 1

even_nums = [num for num in nums if num % 2 == 0]
odd_nums = [num for num in nums if num % 2 != 0]

print("Even count:", even_cnt)
print("Odd count:", odd_cnt)
print("Even numbers:", even_nums)
print("Odd numbers:", odd_nums)

# Question 2

# Test case 1
lst =[10,20,30]
total_no = 3
def calculate_avg(numbers:list) ->float:
  try:
    sum = 0
    for i in lst:
      sum += i
      i += 1
    avg = sum / total_no
    print(f"Average of {lst}: {avg}")

  except ZeroDivisionError:
    print("Sum cannot divide by zero")

calculate_avg(lst)

# test case 2
lst =[]
total_no = 0
def calculate_avg(numbers:list) ->float:
  try:
    sum = 0
    for i in lst:
      sum += i
      i += 1
    avg = sum / total_no
    print(f"Average of {lst}: {avg}:.2f")

  except ZeroDivisionError:
    print("Sum cannot divide by zero")

calculate_avg(lst)

# Question 3

# Test case 1
import random as rd
import math

right_num = rd.randint(1,50)
guess_list =[]

for guesses in range(1, 11):
  num = int(input("Guess the number btwn (1,50): "))
  if num > right_num:
    print("too high!!")
    guess_list.append(num)
  elif num < right_num:
    print("too small!!")
    guess_list.append(num)
  else:
    break
if num == right_num:
  print("You guess the correct number!!")

else:
  print(f"wrong guess , right guess is {right_num}")
print(guess_list)

max = max(guess_list)
print(f"Max guess {max}")

sum = 0
for i in guess_list:
  sum += i
  avg = sum / len(guess_list)
print(f'Average {avg}')

# Question 4

class Student:
    def __init__(self, name: str, marks: list):
        self.name: str = name
        self.marks: list = marks

    def average(self) -> float:
        total = 0
        for i in self.marks:
            total += i

        return total / len(self.marks)

    def __str__(self):
        return f"{self.name}: average {self.average():.1f}"

students = [
    Student("Sakshi", [80, 85, 82]),
    Student("Gaurav", [90, 88, 92]),
    Student("Rahul", [75, 78, 80])
]

for student in students:
    print(student)

highest_student = students[0]

for student in students:
    if student.average() > highest_student.average():
        highest_student = student

print("Highest average:", highest_student.name)



# Question 5

import random as rd

count = 0
nums = [1, 2, 3, 4, 5, 6]

while True:
    # choose random number from nums
    dice = rd.choice(nums)

    count += 1
    print("Dice:", dice)

    if dice == 6:
        break

# generate random no
bonus = rd.randint(1, 10)

print("Number of rolls:", count)
print("Bonus number:", bonus)

