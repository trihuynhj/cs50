// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Convert a string to a double using atof()
    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    //    Declare a header sized array of 1-byte (8-bit) elemenents
    uint8_t header[HEADER_SIZE];
    //    Read into the input file, with the size of 1 byte and the quantity of header size
    //    and store that data into the array
    fread(header, sizeof(uint8_t), HEADER_SIZE, input);
    //    Then write that array to the output file, 1 byte at a time for header size of data
    fwrite(header, sizeof(uint8_t), HEADER_SIZE, output);

    // TODO: Read samples from input file and write updated data to output file
    // Note to self: The position of the file pointer is automatically updated after
    //               the read operation, so the successive read operation should read
    //               the successive pointer
    int16_t buffer;
    while (fread(&buffer, sizeof(uint16_t), 1, input))
    {
        buffer *= factor;
        fwrite(&buffer, sizeof(uint16_t), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);
}
