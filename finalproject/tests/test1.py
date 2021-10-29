# PASSWORD VALIDATION TEST (REGULAR EXPRESSION)

import re

string = input("Provide a string: ")

result1 = re.findall("[0-9]", string)
result2 = re.findall("[!@#$%^&*()_+]", string)

if not result1 and not result2:
    print("No numbers and/or special symbols")
elif not result1 and result2:
    print("No numbers, but has special symbols")
elif result1 and not result2:
    print("No symbols, but has numbers")
else:
    print(result1, result2)