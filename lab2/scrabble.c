#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    // Two arrays that store the decimal values of the alphabet
    int upper[26];
    int lower[26];
    for (int i = 0; i <= 25; i++)
    {
        upper[i] = 65 + i;
        lower[i] = 97 + i;
    }

    // TODO: Compute and return score for string
    int pt = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        int pos = 0;
        bool check = false;
        // If the character is an upper case
        if (isupper(word[i]) > 0)
        {
            while (!check)
            {
                if (word[i] == upper[pos])
                {
                    check = true;
                    pt += POINTS[pos];
                }
                pos++;
            }
        }
        // If the character is a lower case
        else if (islower(word[i]) > 0)
        {
            while (!check)
            {
                if (word[i] == lower[pos])
                {
                    check = true;
                    pt += POINTS[pos];
                }
                pos++;
            }
        }

        // Do nothing if the character is non-alphabet
    }

    return pt;
}