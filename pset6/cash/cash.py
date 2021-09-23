from cs50 import get_float
from math import floor

# Declare the number of coins and the reference set of coins
numCoins = 0
coins = [25, 10, 5, 1]

# Prompt the user input, re-prompt if user input is a negative number
change = get_float("Change owned: ")
change = round(change * 100)
while change < 0:
    change = get_float("Change owned: ")

# Calculate the number of coins from larger coins downward
for i in coins:
    if change >= i:
        _tmp = floor(change / i)
        numCoins += _tmp
        change = change - (_tmp * i)

# Output the result
print(numCoins)
