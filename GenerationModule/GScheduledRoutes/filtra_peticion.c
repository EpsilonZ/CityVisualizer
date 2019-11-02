#include <string.h>
#include <stdio.h>

int main (int argc, char **argv) {
   FILE *fp;
   int c;
   fp = fopen("rutaEjemplo.json","r");
   fseek(fp,0L,SEEK_END);
   int sizeTotal = ftell(fp);
   char aux[ftell(fp)];
   fseek(fp,38,SEEK_SET);
   int cont= 0;	
   while(1) {
      c = fgetc(fp);
	  aux[cont] = c;
      if( feof(fp) ) {
         break;
      }
  //    printf("%c", c);
	  ++cont;
   }
	
   char * res = strtok(aux,"type");
  
   int conta = strlen(res);
  
   res[conta-1] = '\0'; //eliminamos los dos ultimos caracteres
   res[conta-2] = '\0';

//   printf("%s",res);

  
   fclose(fp);
    
   int ret = remove("rutaEjemplo.json");
   FILE *fnou;
   fnou = fopen(argv[1],"a");
   //printf("Res: %s", res);
   fprintf(fnou,"%s",res);
   fprintf(fnou,"%s","\n");

   fclose(fnou);
  
   return(0);
}
