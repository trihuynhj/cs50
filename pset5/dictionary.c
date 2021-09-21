// Implements a dictionary's functionality

#include <stdbool.h>
#include "dictionary.h"
#include <cs50.h>
#include <strings.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 143091 / 2;

// Hash table
node *table[N];

// A counter to count number of words in dictionary
int counter = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash the word to obtain the hash value
    unsigned int h = hash(word);

    // Check if the hash value location in the hash table is empty
    if (table[h] == NULL)
    {
        return false;
    }

    // Otherwise, loop through the nodes at that location
    else
    {
        node *tmp = table[h];

        while (tmp != NULL)
        {
            if (strcasecmp(tmp->word, word) == 0)
            {
                return true;
            }
            else
            {
                tmp = tmp->next;
            }
        }
    }
    // If the program reaches this, it means no node has the word, so return false
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Credit: djb2 hash function created by Dan Bernstein
    unsigned int hash = 5381;
    int c = tolower(*word);

    while (c)
    {
        hash = ((hash << 5) + hash) + c;
        c    = tolower(*word++);
    }

    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    // Read from the file, one string at a time
    char s[LENGTH + 1];
    while (fscanf(file, "%s", s) != EOF)
    {
        // Create a new node for the word
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        strcpy(n->word, s);
        n->next = NULL;

        // Hash word to obtain hash value
        int h = hash(s);

        // Insert node into hash table at the hash value location
        // Case 1: If the current linked list is empty, directly insert the word node into it
        if (table[h] == NULL)
        {
            table[h] = n;
            counter++;
        }
        // Case 2: If the current linked list already contains some other node(s)
        else
        {
            // Point the word node to whatever the head of list is currently pointing at
            n->next = table[h];
            // Redirect the head's pointer to the word node
            table[h] = n;
            counter++;
        }
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Loop through every index of the hash table to check for existing linked lists
    for (int i = 0; i < N; i++)
    {
        // Free memory for each node in the linked list
        while (table[i] != NULL)
        {
            node *tmp = table[i]->next;
            free(table[i]);
            table[i] = tmp;
        }
    }

    return true;
}
