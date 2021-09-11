#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int startsize;
    do
    {
        startsize = get_int("Start size: ");
    }
    while (startsize < 9);

    // TODO: Prompt for end size
    int endsize;
    do
    {
        endsize = get_int("End size: ");
    }
    while (endsize < startsize);

    // TODO: Calculate number of years until we reach threshold
    int year = 0;
    while (startsize < endsize)
    {
        int tmp_born        = startsize / 3;
        int tmp_passaway    = startsize / 4;
        startsize           = startsize + tmp_born - tmp_passaway;
        year++;
    }

    // TODO: Print number of years
    printf("Years: %i\n", year);
}