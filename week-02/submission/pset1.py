#A.1 Create a list containing any 4 strings.
list1=['time','flower','sigh','omg']
#A.2 Print the 3rd item in the list - remember how python indexes lsits!
print(list1[2])
#A.3 Print the 1st and 2nd item in the list using [:] index slicing.
print(list1[:2])
#A.4 Add a new string with text "last" to  the end of the list and print the list.
list1.append('last')
print(list1)
#A.5 Get the list length and print it.
print(len(list1))
#A.6 Replace the last item in the list with the string "new" and print.
list1[4]="new"
print(list1)

sentence_words = ['I', 'am', 'learning', 'Python', 'to', 'munge', 'large', 'datasets', 'and', 'visualize', 'them']
#B.1 Convert the list into a normal sentence with join(), then print.
print(" ".join(sentence_words))
#B.2 Reverse the order of this list using the .reverse() method, then print. Your output should begin with [“them”, ”visualize”, … ].
sentence_words.reverse()
print(sentence_words)
#B.3 Now user the .sort() method to sort the list using the default sort order.
sentence_words.sort()
print(sentence_words)
#B.4 Perform the same operation using the sorted() function. Provide a brief description of how the sorted() function differs from the .sort() method.
print(sorted(sentence_words))
#the sorted() function and .sort() methods differ in that the function is done on the list and returned into a new list, while the method modifies the current list. The function also requires the list as a variable, while the method implicitly passes the list.
#B.5 Extra Credit: Modify the sort to do a case case-insensitive alphabetical sort.
sentence_words.sort(key=lambda s: s.lower())
print(sentence_words)

#C Random Function
from random import randint

def random_it(high, low=0):
    return(randint(low,high))
    print(randint(low,high))

random_it(100)

assert(0 <= random_it(100) <= 100)
assert(50 <= random_it(100, low=50) <= 100)
random_it(300,200)

#D String Formatting function
def bestseller_string(movietitle, n):
    return f"The number {n} bestseller today is: {movietitle.title()}"
    print(f"The number {n} bestseller today is: {movietitle.title()}")

bestseller_string("amazing movie", 1)

#E Password Validation Function
password = input("Please create a password.")
def length_test(x):
    if 8 <= len(x) <= 14:
        return True
    else:
        return False
def digit_test(y):
    digit_count = 0
    for i in y:
        if i.isdigit():
            digit_count += 1
    if digit_count >=2:
        return True
    else:
        return False
def uppercase_test(z):
    for i in z:
        if i.isupper():
            return True
    return False
def special_test(w):
    for i in w:
        if i in ['!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=']:
            return True
    return False
if length_test(password) == False:
    print("Password must be 8-14 charcaters long.")
if digit_test(password) == False:
    print("Password must include at least 2 digits.")
if uppercase_test(password) == False:
    print("Password must include at least 1 uppercase letter.")
if special_test(password) == False:
    print("Password must include at least 1 special character.")
if length_test(password) and digit_test(password) and uppercase_test(password) and special_test(password):
    print("Password is successful!")

#F Exponentiation Function
def exp(x, y):
    exp_result = x
    for i in range(y-1):
        exp_result *= x
    return exp_result
exp(5,4)

#G Min and Max Functions
def what_is_min(somelist):
    minimum = somelist[0]
    for i in somelist:
        if i < minimum:
            minimum = i
    return minimum
def what_is_max(otherlist):
    maximum = otherlist[0]
    for i in otherlist:
        if i > maximum:
            maximum = i
    return maximum
