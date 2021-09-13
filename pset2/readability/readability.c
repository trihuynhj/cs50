#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

// Hint the helper function to get data from the input sentence
int get_letters(string atext);
int get_words(string atext);
int get_sentences(string atext);

int main(void)
{
    // Get the text input from the user
    string input = get_string("Text: ");

    // Get the number of letters, words and sentences of the input text
    int letterCount = get_letters(input);
    int wordCount = get_words(input);
    int sentenceCount = get_sentences(input);

    // Calculate the Coleman-Lau index using the number of letters, words and sentences
    float L = (letterCount * 100.0) / wordCount;
    float S = (sentenceCount * 100.0) / wordCount;
    int colemanLauIndex = round(0.0588 * L - 0.296 * S - 15.8);

    // Output the approximate grade level
    if (colemanLauIndex < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (colemanLauIndex >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", colemanLauIndex);
    }
}

// Helper function to get the number of letters in input text
int get_letters(string atext)
{
    int letters = 0;
    for (int i = 0; i < strlen(atext); i++)
    {
        if ((atext[i] >= 65 && atext[i] <= 90) ||
            (atext[i] >= 97 && atext[i] <= 122))
        {
            letters++;
        }
    }
    return letters;
}

// Helper function to get the number of words in input text
int get_words(string atext)
{
    int words = 1;
    for (int i = 0; i < strlen(atext); i++)
    {
        if (atext[i] == ' ')
        {
            words++;
        }
    }
    return words;
}

// Helper function to get the number of sentences in input text
int get_sentences(string atext)
{
    int sentences = 0;
    for (int i = 0; i < strlen(atext); i++)
    {
        if (atext[i] == '.' || atext[i] == '!' || atext[i] == '?')
        {
            sentences++;
        }
    }
    return sentences;
}