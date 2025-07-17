#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // تأكد من وجود اسم الملف كمُعطى
    if (argc != 2)
    {
        printf("Usage: ./recover filename\n");
        return 1;
    }

    // حاول فتح الملف المُعطى
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open %s\n", argv[1]);
        return 1;
    }

    BYTE buffer[512];
    FILE *img = NULL;
    int file_count = 0;
    char filename[8];

    while (fread(buffer, 1, 512, file) == 512)
    {
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (img != NULL)
            {
                fclose(img);
            }

            sprintf(filename, "%03i.jpg", file_count);
            img = fopen(filename, "w");
            file_count++;
        }

        if (img != NULL)
        {
            fwrite(buffer, 1, 512, img);
        }
    }

    if (img != NULL)
    {
        fclose(img);
    }

    fclose(file);
    return 0;
}
