#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef int16_t sample;

int main(int argc, char *argv[])
{
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open input file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        fclose(input);
        printf("Could not open output file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    uint8_t header[44];
    fread(header, sizeof(uint8_t), 44, input);
    fwrite(header, sizeof(uint8_t), 44, output);

    sample buffer;
    while (fread(&buffer, sizeof(sample), 1, input))
    {
        buffer = buffer * factor;
        fwrite(&buffer, sizeof(sample), 1, output);
    }

    fclose(input);
    fclose(output);
    return 0;
}
