#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define GENERATIONS 3

typedef struct person
{
    struct person *parents[2];
    char alleles[2];
}
person;

person *create_family(int generations);
void print_family(person *p, int generation);
void free_family(person *p);
char random_allele();

int main(void)
{
    // تعيين بداية العشوائية
    srand(time(0));

    // أنشئ شجرة العائلة
    person *p = create_family(GENERATIONS);

    // اطبع الشجرة
    print_family(p, 0);

    // حرّر الذاكرة
    free_family(p);
}

// إنشاء شجرة العائلة بشكل تكراري
person *create_family(int generations)
{
    // تخصيص مساحة لذاكرة شخص
    person *new_person = malloc(sizeof(person));

    // قاعدة التوقف: الجيل الأول
    if (generations > 1)
    {
        // أنشئ الوالدين تكراريًا
        new_person->parents[0] = create_family(generations - 1);
        new_person->parents[1] = create_family(generations - 1);

        // كل والد يعطي أليل عشوائي من الأليلين اللي عنده
        new_person->alleles[0] = new_person->parents[0]->alleles[rand() % 2];
        new_person->alleles[1] = new_person->parents[1]->alleles[rand() % 2];
    }
    else
    {
        // إذا ما فيه والدين، الأليلات تولد عشوائيًا
        new_person->parents[0] = NULL;
        new_person->parents[1] = NULL;
        new_person->alleles[0] = random_allele();
        new_person->alleles[1] = random_allele();
    }

    return new_person;
}

// طباعة شجرة العائلة
void print_family(person *p, int generation)
{
    // إهمال إن كان الشخص NULL
    if (p == NULL)
    {
        return;
    }

    // تحكّم في المسافة حسب الجيل
    for (int i = 0; i < generation * 4; i++)
    {
        printf(" ");
    }

    // عرّف الجيل
    printf("Generation %i, blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);

    // طباعة الأبوين
    print_family(p->parents[0], generation + 1);
    print_family(p->parents[1], generation + 1);
}

// تحرير الذاكرة تكراريًا
void free_family(person *p)
{
    if (p == NULL)
    {
        return;
    }

    free_family(p->parents[0]);
    free_family(p->parents[1]);

    free(p);
}

// اختيار أليل عشوائي
char random_allele()
{
    int r = rand() % 3;
    switch (r)
    {
        case 0:
            return 'A';
        case 1:
            return 'B';
        default:
            return 'O';
    }
}
