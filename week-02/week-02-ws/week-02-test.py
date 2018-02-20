import math
from math import pi

# Dynamic typing!
i=4.0
#floating point data type
print(i)
j=1
print(j)
text = "I'm going to be a string when I grow up"
print(text)
text[0]
#python is zero index
print(math.pi)
print(pi)
type(text)
#variable_name.method()
j.bit_length()
p=4.2
p.is_integer()

f=4.0
f.is_integer()

number=7
number_dec=3.6

result=number+number_dec
print(result)
dedication="Your planet, love."
dedication[0:4]
#second number is exclusive, not inclusive
dedication_supp="Your reality, honey."
paean = dedication+" "+dedication_supp
print(paean)
paean.find("love")
paean[13]
paean_length=2
#F STRING
msg = f"I wrote you a paean. It goes like {dedication}. Then it goes like {dedication_supp}. It has {paean_length} lines."
print(msg)

#Boolean
reality = True
non_reality = False

print(reality and not non_reality)

eric_height = 6.0
liana_height = 5.75

print(eric_height>liana_height)
print(eric_height==liana_height)

#LIST
l_one=[]

x=5
l_two=[1,2.0,'a',"abcd",True,x]
l_two[2]

l_two.append(1)
print(l_two)

l_three=['a','b','c']

l_two.append(l_three)

print(l_two)

l_two.extend(l_three)
print(l_two)

squares=[]
for i in range(5):
    squares.append(i*i)
print(squares)

#Dictionaries
# key:value pairs
d_one={'key1':1,'key2':"moose",'key3':4}
print(d_one)
d_one['key1']
print(math.pi)
import panda as pd
