# PASSWORD VALIDATION TEST (REGULAR EXPRESSION)

import re

string = input("Provide a string: ")

result1 = re.findall("[0-9]", string)
result2 = re.findall("[!@#$%^&*()_+]", string)