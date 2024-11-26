#include <stdio.h>

int main(void) {
    char capital[] = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
                      'Q','R','S','T','U','V','W','X','Y','Z'};
    char small[] = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
                    'q','r','s','t','u','v','w','x','y','z'};
    
    char input;

    do {
        printf("Enter 'U'/'u' for uppercase or 'L'/'l'for lowercase: ");
        scanf(" %c", &input);

        if (input == 'U' || input == 'u') {
            int ii= 0;
            do{
                printf("%c ",capital[ii]);
                ii++;
            }while(ii < 26);
            printf("\n");
        } 
        else if (input == 'L' || input == 'l') {
            int ii= 0;
            do{
                printf("%c ",small[ii]);
               
                ii++;
            }while(ii < 26);
            printf("\n");
        } 
        else {
            printf("Thank you\n");
            break; 
        }
    } while (1);

    return 0;
}
