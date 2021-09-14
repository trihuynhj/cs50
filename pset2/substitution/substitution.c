#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

// Initiate a helper funtion that encrypts the input text using the key
string encrypt(string text, string keyword);

int main(int argc, string argv[])
{
    // Print out error message if the user input 0 or more than 1 command-line arguments
    if (argc != 2)
    {
        printf("Key is invalid.\n");
        return 1;
    }

    // Copy the command-lind argument into a variable
    string key = argv[1];

    // Print out error message if the key does not have exactly 26 characters
    if (strlen(key) != 26)
    {
        printf("Invalid. Key must contains exactly 26 characters.\n");
        return 1;
    }

    // Print out error message if the key contains non-alphabetic characters
    for (int i = 0; i < strlen(key); i++)
    {
        if ((key[i] < 65) || (key[i] >= 91 && key[i] <= 96) || (key[i] > 122))
        {
            printf("Invalid. Key must contains only alphabet letters.\n");
            return 1;
        }
    }

    // Convert all key's characters to lower case for ease of computation
    for (int i = 0; i < strlen(key); i++)
    {
        if (islower(key[i]) == 0)
        {
            key[i] += 32;
        }
    }

    // Print out error message if there are duplicated alphabet characters
    for (int i = 0; i < strlen(key); i++)
    {
        for (int j = i + 1; j < strlen(key); j++)
        {
            if (key[i] == key[j])
            {
                printf("Invalid. There are duplicated letters in the key.\n");
                return 1;
            }
        }
    }

    // Get plaintext input from user
    string plain_text = get_string("plaintext: ");
    string cipher_text = encrypt(plain_text, key);

    // Print out the encrypted ciphertext
    printf("ciphertext: %s\n", cipher_text);

}

// Helper function to convert the plaintext into ciphertext using the input key
string encrypt(string text, string keyword)
{
    // Initiate the alphabet array
    char alphabet[26];
    for (int i = 0; i < 26; i++)
    {
        alphabet[i] = 97 + i;
    }

    // Copy the original text to a new variable to avoid side effects
    string encrypted_text = text;

    // Loop through the text, check, convert using key and replace the original character
    // with the encrypted character into the new string (case-sentitive)
    for (int j = 0; j < strlen(text); j++)
    {
        char letter = text[j];
        if (islower(letter) > 0)
        {
            int k = 0;
            while (letter != alphabet[k])
            {
                k++;
            }
            letter = keyword[k];
        }
        else if (isupper(letter) > 0)
        {
            int k = 0;
            while (letter != alphabet[k] - 32)
            {
                k++;
            }
            letter = keyword[k] - 32;
        }
        encrypted_text[j] = letter;
    }

    return encrypted_text;
}