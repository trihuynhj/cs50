#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Declare a new pointer with RGBTRIPLE type
    RGBTRIPLE *pixel;
    double avgVal;

    // Loop through each pixel
    for (int i = 0; i < height; i++)
    {
        // Assign to pointer the first location (address) of each row
        pixel = &image[i][0];

        // Then move to the next location in the row with a 2nd loop
        for (int j = 0; j < width; j++, pixel++)
        {
            // A pixel is in black-and-white when all 3 RGB values are identical
            // Note-to-self: arrow operation [->] is just like dot operation [.]
            //               but for pointer variables
            avgVal = (pixel->rgbtBlue + pixel->rgbtGreen + pixel->rgbtRed) / 3.0;
            pixel->rgbtBlue = pixel->rgbtGreen = pixel->rgbtRed = round(avgVal);
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Declare a new pointer variable with RGBTRIPLE type
    RGBTRIPLE *pixel;
    double sepiablue, sepiagreen, sepiared;

    // Loop through each pixel
    for (int i = 0; i < height; i++)
    {
        pixel = &image[i][0];
        for (int j = 0; j < width; j++, pixel++)
        {
            // Convert to sepia values using the algorithm provided by CS50 and round them to the nearest integer
            sepiablue  = round(.272 * pixel->rgbtRed + .534 * pixel->rgbtGreen + .131 * pixel->rgbtBlue);
            sepiagreen = round(.349 * pixel->rgbtRed + .686 * pixel->rgbtGreen + .168 * pixel->rgbtBlue);
            sepiared   = round(.393 * pixel->rgbtRed + .769 * pixel->rgbtGreen + .189 * pixel->rgbtBlue);

            // Set the upper limit of each converted value to 255 (max value of a 8-bit color)
            if (sepiablue > 255)
            {
                sepiablue = 255;
            }
            if (sepiagreen > 255)
            {
                sepiagreen = 255;
            }
            if (sepiared > 255)
            {
                sepiared = 255;
            }

            // Put the calculated values back to the current pixel
            pixel->rgbtBlue  = sepiablue;
            pixel->rgbtGreen = sepiagreen;
            pixel->rgbtRed   = sepiared;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE *pixel;
    for (int i = 0; i < height; i++)
    {
        pixel = &image[i][0];
        for (int j = 0; j < width / 2; j++, pixel += 1)
        {
            RGBTRIPLE *opixel = &image[i][width - 1 - j];
            RGBTRIPLE tmp;

            // Store the current pixel in a temp variable
            tmp     = *pixel;

            // Put the opposite pixel into current pixel
            *pixel  = *opixel;

            // Put the temp pixel into opposite pixel
            *opixel = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Use a temporary 2D array to store the blur-converted image
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Declare some new variables to calculate the temp pixel
            float sumBlue = 0, sumGreen = 0, sumRed = 0;
            int num = 0;
            for (int k = i - 1; k < i + 2; k++)
            {
                // Condition k and l to only check values within the image array
                // (to avoid segmentation fault)
                if (k >= 0 && k < height)
                {
                    for (int l = j - 1; l < j + 2; l++)
                    {
                        if (l >= 0 && l < width)
                        {
                            sumBlue     += image[k][l].rgbtBlue;
                            sumGreen    += image[k][l].rgbtGreen;
                            sumRed      += image[k][l].rgbtRed;
                            num++;
                        }
                    }
                }
            }

            // Put the average pixels into the temporary image after each pixel
            temp[i][j].rgbtBlue     = round(sumBlue / num);
            temp[i][j].rgbtGreen    = round(sumGreen / num);
            temp[i][j].rgbtRed      = round(sumRed / num);
        }
    }

    // Replace each pixel in the original image with temp image
    RGBTRIPLE *temppixel;
    RGBTRIPLE *pixel;
    for (int m = 0; m < height; m++)
    {
        temppixel   = &temp[m][0];
        pixel       = &image[m][0];
        for (int n = 0; n < width; n++, temppixel++, pixel++)
        {
            *pixel = *temppixel;
        }
    }
    return;
}
