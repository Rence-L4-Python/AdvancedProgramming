student={'name':'alpha','id':5,'course':'BSc CC'}

## Display key-value pairs
## Display only keys
## Display only values
## Adding new value 'Year_of_entry' = 2022
## Modify Value of course = BSc CS
## Remove Course Key-Value Pair

x= student.items()
y= student.keys()
z= student.values()
print(x)
print(y)
print(z)
student.update({'Year_of_entry':'2022'})
print(student)
student.update({'course':'BSc CS'})
print(student)
del student["course"]
print(student)