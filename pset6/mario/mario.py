from cs50 import get_int


def main():

    # Prompt user input, re-prompt if input is not in range of 1 to 8 inclusive
    height = get_int("Height: ")
    while (height < 1 or height > 8):
        height = get_int("Height: ")

    # Use recursive
    r_pyramid(height, height)


# Use for loop: Generate pyramid from user input
def f_pyramid(h):
    for i in range(h):
        print(' ' * (h - i - 1), end='')
        print('#' * (i + 1), end='')
        print('  ', end='')
        print('#' * (i + 1))


# Use recursive: Generate pyramid from user input
def r_pyramid(currentHeight, originalHeight):
    if currentHeight == 1:
        print(' ' * (originalHeight - 1), end='')
        print('#  #')
    else:
        r_pyramid(currentHeight - 1, originalHeight)
        print(' ' * (originalHeight - currentHeight), end='')
        print('#' * currentHeight, end='')
        print('  ', end='')
        print('#' * currentHeight)


# Simulate a main function like in C
if __name__ == "__main__":
    main()