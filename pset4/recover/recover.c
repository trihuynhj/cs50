#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// Define a block of 512 elements and a new data type of 1 byte (or 8 bits)
const int BLOCK = 512;
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Ensure there is only one command-line argument
    if (argc != 2)
    {
        printf("There must be exactly one command-line argument.\n");
        return 1;
    }

    // Read the input file and ensure it is a valid file
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Invalid input file.\n");
        return 1;
    }

    // Define the buffer and file count
    BYTE buffer[BLOCK];
    int filecount = 0;

    // Check whether the first image has been created
    int checkfirst = 0;

    // Define a new file
    char *filename = malloc(sizeof("xxx.jpg"));
    FILE *img = NULL;

    // Loop through the file one BLOCK at a time
    while (fread(buffer, sizeof(BYTE), BLOCK, input) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Signal that the first JPEG has been found
            if (filecount == 0)
            {
                checkfirst = 1;
            }

            // Create a new image
            sprintf(filename, "%03i.jpg", filecount);
            img = fopen(filename, "w");
            filecount++;

            // Copy the first block to the image
            fwrite(buffer, sizeof(BYTE), BLOCK, img);
        }
        else
        {
            // Copy the current block to the image when and only when
            // the first image has been created (to avoid segmentation fault)
            if (checkfirst == 1)
            {
                fwrite(buffer, sizeof(BYTE), BLOCK, img);
            }
        }
    }

    // Free the memory allocated by malloc
    free(filename);
}
