#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

// Boilerplate for helper functions
string encrypt(string text, int key);
int char_pos(char character);

int main(int argc, string argv[])
{
    // Throw a error if there is 0 or more than 1 command-line arguments.
    if (argc != 2)
    {
        printf("Invalid. There must be exactly one command-line argument.\n");
        return 1;
    }

    // Convert the command-line argument into an integer using stdlib.h function
    int keyword = atoi(argv[1]);

    // Throw an error if the key is not a positive number
    if (keyword < 0)
    {
        printf("Invalid. The key must be a non-negative number.\n");
        return 1;
    }

    // Get the plaintext input from user
    string input = get_string("plaintext:  ");

    // Convert the plaintext to ciphertext using the key and a helper function
    string output = encrypt(input, keyword);

    // Print out the cipher text
    printf("ciphertext: %s\n", output);
}

// Helper function that converts a text to a ciphertext using a key
string encrypt(string text, int key)
{
    // Copy the original string into a new variable to avoid side effects
    string encrypted = text;

    for (int i = 0; i < strlen(text); i++)
    {
        char c = text[i];
        if (c >= 65 && c <= 90)
        {
            encrypted[i] = 65 + (char_pos(c) + key) % 26;
        }
        else if (c >= 97 && c <= 122)
        {
            encrypted[i] = 97 + (char_pos(c) + key) % 26;
        }
    }

    return encrypted;
}

// Helper function that returns the position of a character in an alphabetical order
int char_pos(char character)
{
    char upper_alphabet[26];
    char lower_alphabet[26];
    for (int i = 0; i < 26; i++)
    {
        upper_alphabet[i] = 65 + i;
        lower_alphabet[i] = 97 + i;
    }

    int k = 0;
    if (isupper(character) > 0)
    {
        while (upper_alphabet[k] != character)
        {
            k++;
        }
    }

    else if (islower(character) > 0)
    {
        while (lower_alphabet[k] != character)
        {
            k++;
        }
    }

    return k;
}