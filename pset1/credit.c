#include <stdio.h>
#include <cs50.h>

// Prototypes
int get_digit(long num, int pos);
int get_length(long num);

int main(void)
{
    // Prompt user the input and get the length of the input number
    long n = get_long("Number: ");
    int length = get_length(n);

    // Ensure that the input number is valid
    if (length < 13)
    {
        printf("INVALID\n");
        return 0;
    }

    // Calculate sum of digits from second-to-last digit from right to left
    int sum_odd = 0;
    for (int i = 1; i < length; i += 2)
    {
        // First, multiply the digit by 2
        int tmp = 2 * get_digit(n, i);

        // If the result is a 2-digit value, add each of the digits to sum
        if (tmp > 9)
        {
            sum_odd += get_digit(tmp, 0) + get_digit(tmp, 1);
        }
        // Otherwise, just add that value to sum
        else
        {
            sum_odd += tmp;
        }
    }

    // Calculate the sum of remaining digits
    int sum_even = 0;
    for (int j = 0; j < length; j += 2)
    {
        sum_even += get_digit(n, j);
    }

    // Total sum
    int sum = sum_odd + sum_even;
    // If the last digit of the sum is not a zero, then the number is invalid
    if (sum % 10 != 0)
    {
        printf("INVALID\n");
    }
    // Otherwise, check the type of the number
    else
    {
        // All AMEX cards start with 34 or 37
        if (get_digit(n, length - 1) == 3)
        {
            if (get_digit(n, length - 2) == 4 || get_digit(n, length - 2) == 7)
            {
                printf("AMEX\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }

        // All VISA cards start with 4
        else if (get_digit(n, length - 1) == 4)
        {
            printf("VISA\n");
        }

        // All MASTER cards start with 51, 52, 53, 54 or 55 (just in this problem)
        else if (get_digit(n, length - 1) == 5)
        {
            if (get_digit(n, length - 2) == 1 || get_digit(n, length - 2) == 2 || get_digit(n, length - 2) == 3
                || get_digit(n, length - 2) == 4 || get_digit(n, length - 2) == 5)
            {
                printf("MASTERCARD\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }

        // Return INVALID if the number did not match any of the above cases
        else
        {
            printf("INVALID\n");
        }
    }
}


// Get the digit at the position (counting from 0 from right to left)
int get_digit(long num, int pos)
{
    int value;
    long location = 1;

    for (int i = 0; i < pos; i++)
    {
        location *= 10;
    }

    if (location > num)
    {
        value = -1;
        return value;
    }

    value = (num / location) % 10;
    return value;
}

/// Get the length of a number
int get_length(long num)
{
    int len = 1;
    while (num > 9)
    {
        len++;
        num /= 10;
    }
    return len;
}