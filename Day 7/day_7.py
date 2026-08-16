''' Day 7: Libraries
   Date : 16 -Aug -2026
   Name: Gaurav Bharat Deore
   Contact no : 9373446328
   Email :bharatdeore7813@gmail.com
   Description : Introduction to Libraries like numpy , request 
   Topics : 1)Numpy  ,2) list vs array ,3) numpy operations ,4) Metrics representation
   7)URL, 8) get request , 9) post request
'''

# Libraries
# -Numpy

import math
math.sqrt(64)

def square_rt(x):
  return x ** 0.5
square_rt(64)

"""# Tasks for which the libraries are used:


1.  math and calculation
2.  files
3. database
4. graphs and charts
5. website and the internet
6. machine learning models
7. data processing
8. dates and time

"""

!pip install numpy

import numpy as np

num = np.array([10,20,30])  # numpy array
num

lst = [10,20,30]  # python list
print(lst)
print(type(lst))

"""**Array la apan multiple elements access kru shakto at a time for ex. if i want to sqaure of list then array helps to print the whole list of sqaures of a list**

**Whereas the list , takes single element at once and cant be able to print the whjole list**
"""

num = [10,20,30]
result=[]

for i in num:
  result.append(i * 2)
result

nums = np.array([10,20,30])
result =nums * 2
result

# 3 ways to create an array
np.zeros(5) # print 5 elements of 0

np.ones(5) # print 5 elements of 1

np.arange(0,11,2) #(start, stop,step)

# access and changing the element

nums =[10,20,30]
num[0]
num[1] = 99
num

num= np.array([10,20,30])
num + 5

num= np.array([10,20,30])
num * 2

num= np.array([10,20,30])
num /10

# working with 2 arrays
a = np.array([10,20,30])
b = np.array([5,10,15])

print(a + b)
print(a * b)

# useful numpy func

nums = np.array([10,20,30,50,60])

print(np.sum(nums))
print(np.max(nums))
print(np.mean(nums))

# shape : rows and columns
nums = np.array([
    [1,2,3],
    [4,5,6]
])

print(nums.shape)
print(nums[0,1]) # row,column

# URL
# - python's built in way of urllib


import urllib.request
response =urllib.request.urlopen('https://www.google.com/')
response.status

!pip install requests

# request
import requests
requests.get('https://www.google.com/')

# assignment

# worked example :Student_marks.py

marks = np.array([86,90,78,92,86])
print("Marks:", marks)
print("Total:", np.sum(marks))
print("Average:", np.mean(marks))
print("Highest:", np.max)

# Requests and JSON
# - making get request , and reading it back


res = requests.get('https://www.google.com/')
res.status_code

res.text

res.raise_for_status()  # raises an error automatically on 404,500,etc

# this code provides an error bcz google returns HTML page and we are trying to send data in json

res = requests.get('https://www.google.com/')
data = res.json()
data['name']

"""# Getting JSON data - python objects , not text

# GET vs. POST
- asking vs. sending
"""

# syntax of get request
requests.get(url)

requests.get('https://www.google.com/')

# syntax of post request
requests.post(url, json =data)

requests.post('https://www.google.com/', json = {'text':'hello'})

