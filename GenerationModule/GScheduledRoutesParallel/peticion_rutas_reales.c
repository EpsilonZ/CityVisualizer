#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <math.h>
#include <time.h>
#include <fcntl.h>


#define ANSI_COLOR_GREEN   "\x1b[32m"
#define ANSI_COLOR_RESET   "\x1b[0m"


#define pi 3.14159265358979323846

//Funciones para el calculo de la distancia a partir de dos coordenadas GPS. Extraido de https://www.geodatasource.com 

double deg2rad(double);
double rad2deg(double);

double distance(double lat1, double lon1, double lat2, double lon2, char unit) {
  double theta, dist;
  theta = lon1 - lon2;
  dist = sin(deg2rad(lat1)) * sin(deg2rad(lat2)) + cos(deg2rad(lat1)) * cos(deg2rad(lat2)) * cos(deg2rad(theta));
  dist = acos(dist);
  dist = rad2deg(dist);
  dist = dist * 60 * 1.1515;
  switch(unit) {
    case 'M':
      break;
    case 'K':
      dist = dist * 1.609344;
      break;
    case 'N':
      dist = dist * 0.8684;
      break;
  }
  return (dist);
}

double deg2rad(double deg) {
  return (deg * pi / 180);
}

double rad2deg(double rad) {
  return (rad * 180 / pi);
}





//Tasa de paro en el municipio. La fuente: https://www.datosmacro.com/paro/espana/municipios/cataluna/barcelona/vilanova-i-la-geltru

float tasaParo = 0.1181;


/* Centros educativos. Estos son (en el orden que están implementados):

La Balufa, espai municipal per a la infancia
Llar d'Infants Municipal L'Escateret
Llar d'Infants El Drac
Llar d'Infants El Gavot
Llar d'Infants El Tabal
Llar d'Infants L'Oreneta
Escola bressol La Lluna de Vilanova
Llar d'Infants Xiu-Xiu Jardí
Llar d'Infants Petits Somnis/Little Dreams
Llar d'Infants Estel Platja
Llar d'Infants Mans Manetes
Llar d'Infants El Cau de la Rateta
Escola L'Aragai
Escola L'Arjau
Escola Canigó
Escola Cossetània
Escola Ginesta
Escola Llebetx
Escola El Margalló
Escola Pompeu Fabra
Escola Sant Jordi
Escola Ítaca
Escola Volerany
Escola La Pau
Col·legi Divina Providència
Escola El Cim
Escola Pia Vilanova i la Geltrú
Col·legi Sant Bonaventura
Col·legi Santa Teresa de Jesús
Institut Dolors Mallafrè i Ros
Institut F.X Lluch i Rafecas
Institut Joaquim Mir
Institut Manuel de Cabanyes
Institut Baix a Mar
EPSEVG-UPC Vilanova i la Geltrú
Escola Municipal d'Art i Disseny
Escola Conservatori Municipal Música Mestre i Montserrat

*/

/*float coordenadasCentrosEducativos [36][2] = { {1.71811,41.22727},{1.73148,41.22693},{1.71978,41.21873},{1.73256,41.21808},{1.72833,41.22298},{1.73011,41.22491},{1.71805,41.22286},
								   			   {1.70832,41.2158},{1.72144,41.21586},{1.72948,41.2168},{1.7153,41.22451},{1.71138,41.21801},{1.71241,41.22089},{1.73214,41.21907},
								   			   {1.71917, 41.21865},{1.70835, 41.22397},{1.72641, 41.2326},{1.71463, 41.21336},{1.69498, 41.22776},{1.72282, 41.22162},{1.73111, 41.2277},
								  			   {1.70462, 41.22216},{1.71743, 41.22011},{1.72777, 41.21897},{1.72814, 41.22361},{1.72653, 41.22123},{1.72612, 41.22492},{1.72427, 41.21933},
								 			   {1.70768, 41.219},{1.70807, 41.22492},{1.72587, 41.22242},{1.71106, 41.22215},{1.72794, 41.23116},{1.71731, 41.22167},{1.73391, 41.21909},
								   			   {1.73001, 41.22115} };*/

float coordenadasCentrosEducativos [10][2] = {{1.698466,41.225163},{1.690294,41.221331},{1.699993,41.225366},{1.721580,41.214520},{1.739690,41.227335},{1.682698,41.218490},{1.685359,41.205092},{1.735355,41.231337},{1.738789,41.221267},{1.707761,41.226915}};


float horarioCentrosEducativos [10][2] = { {9,17},{9,15},{7.30,18},{9,12.30},{8,13.30},{8,14.30},{8,14.30},{8.30,12.30},{7,19},{8,14.30} };

int edadesPorCentro [10][2] = {{0,24},{3,11},{3,11},{3,11},{3,16},{3,18},{3,21},{11,21},{11,24},{18,24}};

/*float horarioCentrosEducativos [36][2] = { {9,17}, {9,17}, {9,15}, {9,17}, {7,19}, {7.30,18}, {9,17}, {7.30,18}, {9,13}, {7.30,18}, {7,16}, {7,18}, {9,12.30}, {9,13}, {9,12.30}, {9,12.30}, 												   {9,12.30}, {8.30,12.30}, {9,12.30}, {9,12.30}, {9,12.30}, {9,12.30}, {9,12.30}, {9,12.30}, {9,13}, {8,13.30}, {8,13.30}, {8,15}, {8,13.30}, {8,13.30}, 												   {8,14.30}, {8,14.30}, {8,14.30}, {8,14.30}, {8,14.30}, {8,14.30} };


int edadesPorCentro [36][2] = { {0,3}, {0,3}, {0,3}, {0,3}, {0,3}, {0,3}, {0,3}, {0,3}, {0,3}, {0,3}, {0,3}, {0,3}, {3,11}, {3,11}, {3,11}, {3,11}, {3,11}, {3,11}, {3,11}, {3,11}, {3,11}, {3,11}, 	{3,11}, {3,16}, {3,16}, {3,18}, {3,16}, {3,21}, {11,18}, {11,21}, {11,21}, {11,21}, {11,21}, {18,24}, {11,24}, {11,24} };*/



/*Lugares de trabajo. En este momento tenemos:

Todos los centros educativos
Ayuntamiento de Vilanova i la Geltrú (horario inventado)
Policia Nacional (horario inventado)
Policia Local (horario inventado)
Peluquería (horario inventado)

*/

float coordenadasCentrosTrabajo [10][2] = {{1.696801,41.224012}, {1.701366,41.215391}, {1.699993,41.225366},{1.721580,41.214520},{1.739690,41.227335},{1.682698,41.218490},{1.685359,41.205092},{1.735355,41.231337},{1.738789,41.221267},{1.707761,41.226915}};


float horarioLugaresTrabajo [10][2] = { {6.20,14},{9,15},{7.30,18},{9,12.30},{8,13.30},{8,14.30},{8,14.30},{8.30,12.30},{7,19},{8,14.30} };

/*
float coordenadasCentrosTrabajo [40][2] = { {1.71811,41.22727},{1.73148,41.22693},{1.71978,41.21873},{1.73256,41.21808},{1.72833,41.22298},{1.73011,41.22491},{1.71805,41.22286},
								   			   {1.70832,41.2158},{1.72144,41.21586},{1.72948,41.2168},{1.7153,41.22451},{1.71138,41.21801},{1.71241,41.22089},{1.73214,41.21907},
								   			   {1.71917, 41.21865},{1.70835, 41.22397},{1.72641, 41.2326},{1.71463, 41.21336},{1.69498, 41.22776},{1.72282, 41.22162},{1.73111, 41.2277},
								  			   {1.70462, 41.22216},{1.71743, 41.22011},{1.72777, 41.21897},{1.72814, 41.22361},{1.72653, 41.22123},{1.72612, 41.22492},{1.72427, 41.21933},
								 			   {1.70768, 41.219},{1.70807, 41.22492},{1.72587, 41.22242},{1.71106, 41.22215},{1.72794, 41.23116},{1.71731, 41.22167},{1.73391, 41.21909},
								   			   {1.73001, 41.22115}, {1.72603,41.22416}, {1.726208,41.22483}, {1.722106,41.221477}, {1.720831,41.223694} };

float horarioLugaresTrabajo[40][2] = { {9,17}, {9,17}, {9,15}, {9,17}, {7,19}, {7.30,18}, {9,17}, {7.30,18}, {9,13}, {7.30,18}, {7,16}, {7,18}, {9,12.30}, {9,13}, {9,12.30}, {9,12.30}, 											{9,12.30}, {8.30,12.30}, {9,12.30}, {9,12.30}, {9,12.30}, {9,12.30}, {9,12.30}, {9,12.30}, {9,13}, {8,13.30}, {8,13.30}, {8,15}, {8,13.30}, {8,13.30}, 										    {8,14.30}, {8,14.30}, {8,14.30}, {8,14.30}, {8,14.30}, {8,14.30}, {7,17}, {6,14}, {7,20}, {8,19} };

*/

//0: Parc enveja
//1: camp de vilanova i la geltru futbol
//2: pistas atletismo
//3: parc de baixamar
//4: plaza calganeta
//5: plaza sardana
//6: parque guma i ferran

float coordenadasLudico [7][2] = { {1.699865,41.225515}, {1.7314,41.2329}, {1.7345,41.2315}, {1.7251,41.2171}, {1.72152,41.22387}, {1.72191,41.21798}, {1.72474,41.21865} };
	


float float_rand( float min, float max )
{
    float scale = rand() / (float) RAND_MAX; /* [0, 1.0] */
    return min + scale * ( max - min );      /* [min, max] */
}

float hora_aleatoria (int min, int max){

	int hora = rand()%(max-min + 1) + min;
	
	float minutos = float_rand(0,0.59);

	float horaReturn = hora + minutos;


	return horaReturn;
}


int esta_dentro_barrio(int nvert, float *vertx, float *verty, float testx, float testy) // Info del algoritmo --> https://wrf.ecse.rpi.edu//Research/Short_Notes/pnpoly.html
//Funcion para comprobar que las coordenadas estan dentro del barrio
{
  int i, j, c = 0;
  for (i = 0, j = nvert-1; i < nvert; j = i++) {
    if ( ((verty[i]>testy) != (verty[j]>testy)) &&
     (testx < (vertx[j]-vertx[i]) * (testy-verty[i]) / (verty[j]-verty[i]) + vertx[i]) )
       c = !c;
  }
  return c;
}


float * retorna_coordenadas_barrio (int i, float *porcentaje, int *size){

	float *arr;
	//Todos los barrios de Vilanova segun su distribucion demografica 
	
	if(i==0){
		arr = malloc(8*sizeof(float));
		//L'Aragai
		(*size) = 8;
		arr[0] = 1.7043;
		arr[1] = 41.2208;
		arr[2] = 1.6976;
		arr[3] = 41.2156;
		arr[4] = 1.70055;
		arr[5] = 41.2127;
		arr[6] = 1.7079;
		arr[7] = 41.2155;
		(*porcentaje) = 8.3823 / 100;
	}
	else if(i==1){
		arr = malloc(8*sizeof(float));
		//L'Armanyà
		(*size) = 8;
		arr[0] = 1.72418;
		arr[1] = 41.23307;
		arr[2] = 1.72748;
		arr[3] = 41.2332;
		arr[4] = 1.72795;
		arr[5] = 41.2305;
		arr[6] = 1.72479;
		arr[7] = 41.2304;
		(*porcentaje) = 2.6057 / 100;
	}
	else if(i==2){
		arr = malloc(8*sizeof(float));
		//Barri de Mar
		(*size) = 8;
		arr[0] = 1.7212;
		arr[1] = 41.2204;
		arr[2] = 1.7394;
		arr[3] = 41.2249;
		arr[4] = 1.7417;
		arr[5] = 41.2192;
		arr[6] = 1.7243;
		arr[7] = 41.2144;
		(*porcentaje) = 12.650821561 / 100;
	}
	else if(i==3){
		arr = malloc(8*sizeof(float));
		//Can Marquès
		(*size) = 8;
		arr[0] = 1.723;
		arr[1] = 41.2225;
		arr[2] = 1.7245;
		arr[3] = 41.2229;
		arr[4] = 1.7243;
		arr[5] = 41.2203; 
		arr[6] = 1.7257;
		arr[7] = 41.2208;
		(*porcentaje) = 1.105 / 100;
	}
	else if(i==4){
		arr = malloc(8*sizeof(float));
		//Casernes
		(*size) = 8;
		arr[0] = 1.7249;
		arr[1] = 41.2285;
		arr[2] = 1.7244;
		arr[3] = 41.2301;
		arr[4] = 1.7297;
		arr[5] = 41.2305;
		arr[6] = 1.7303;
		arr[7] = 41.2285;
		(*porcentaje) = 2.0175 / 100;
	}
	else if(i==5){
		arr = malloc(8*sizeof(float));
		//Centrevila
		(*size) = 8;
		arr[0] = 1.72803;
		arr[1] = 41.22741;
		arr[2] = 1.7195;
		arr[3] = 41.2248;
		arr[4] = 1.7258;
		arr[5] = 41.2207;
		arr[6] = 1.733; 
		arr[7] = 41.223;


		(*porcentaje) = 6.996907779 / 100;
	}
	else if(i==6){
		arr = malloc(20*sizeof(float));
		//La Collada - Els Sis Camins
		(*size) = 20;

		arr[0] = 1.7037;
		arr[1] = 41.2202;

		arr[2] = 1.7096;
		arr[3] = 41.224;

		arr[4] = 1.7076; 
		arr[5] = 41.2259;

		arr[6] = 1.7025;
		arr[7] = 41.2254;

		arr[8] = 1.6973;
		arr[9] = 41.2284; 

		arr[10] = 1.6913;
		arr[11] = 41.2302;

		arr[12] = 1.6916;
		arr[13] = 41.2259;

		arr[14] = 1.6934;
		arr[15] = 41.2233;

		arr[16] = 1.6963;
		arr[17] = 41.2206;

		arr[18] = 1.7005;
		arr[19] = 41.2228;

	//	arr[6] = 1.6914;
	//	arr[7] = 41.23;

	//	arr[8] = 1.6917;
	//	arr[9] = 41.2259;

	//	arr[10] = 1.6959;
	//	arr[11] = 41.2216;

		(*porcentaje) = 5.901 / 100;
	}
	else if(i==7){
		arr = malloc(10*sizeof(float));
		//Fondo Somella
		(*size) = 10;
		arr[0] = 1.6961; 
		arr[1] = 41.222;
		arr[2] = 1.6933;
		arr[3] = 41.2239;
		arr[4] = 1.6854;
		arr[5] = 41.2207;
		arr[6] = 1.6916;
		arr[7] = 41.2152;
		arr[8] = 1.6956;
		arr[9] = 41.2169;

		(*porcentaje) = 1.2733 / 100;
	}
	else if(i==8){
		arr = malloc(8*sizeof(float));
		//La Geltrú
		(*size) = 8;
		arr[0] = 1.7238;
		arr[1] = 41.2213;
		arr[2] = 1.7337;
		arr[3] = 41.2364;
		arr[4] = 1.7461;
		arr[5] = 41.2222;
		arr[6] = 1.7242;
		arr[7] = 41.2203;

		(*porcentaje) = 15.0852 / 100;
	}
	else if(i==9){
		arr = malloc(8*sizeof(float));
		//Masia Nova
		(*size) = 8;
		arr[0] = 1.74;
		arr[1] = 41.23077;
		arr[2] = 1.74045;
		arr[3] = 41.22994;
		arr[4] = 1.74279;
		arr[5] = 41.23094;
		arr[6] = 1.74235;
		arr[7] = 41.23181;
		(*porcentaje) = 0.4593 / 100;
	}
	else if(i==10){
		arr = malloc(8*sizeof(float));
		//Moli de vent
		(*size) = 8;
		arr[0] = 1.7034;
		arr[1] = 41.2206;
		arr[2] = 1.7106;
		arr[3] = 41.2247;
		arr[4] = 1.7165;
		arr[5] = 41.2185;
		arr[6] = 1.7079;
		arr[7] = 41.215;

		(*porcentaje) = 9.4131 / 100;
	}
	else if(i==11){
		//Nucli Antic
//41.22741, 1.72803
		arr = malloc(8*sizeof(float));
		(*size) = 8;
		arr[0] = 1.7167;
		arr[1] = 41.2278;
		arr[2] = 1.7198;
		arr[3] = 41.2246;
		arr[4] = 1.72803;
		arr[5] = 41.22741;
		arr[6] = 1.72203;
		arr[7] = 41.22998;


		(*porcentaje) = 6.9241 / 100;	
	}
	else if(i==12){
		arr = malloc(10*sizeof(float));		
		//Plaça de la Sardana
		(*size) = 10;
		arr[0] = 1.7238; 
		arr[1] = 41.2212;
		arr[2] = 1.7255; 
		arr[3] = 41.2185;
		arr[4] = 1.7227; 
		arr[5] = 41.2174;
		arr[6] = 1.7163;
		arr[7] = 41.219;
		arr[8] = 1.7252;
		arr[9] = 41.2216;
		(*porcentaje) = 6.0768 / 100;
	}
	else if(i==13){
		arr = malloc(8*sizeof(float));
		//Prat de Vilanova
		(*size) = 8;
		arr[0] = 1.6818;
		arr[1] = 41.2052;
		arr[2] = 1.6872;
		arr[3] = 41.2064;
		arr[4] = 1.6876;
		arr[5] = 41.2048;
		arr[6] = 1.6829;
		arr[7] = 41.2028;
		(*porcentaje) = 0.6897 / 100;
	}
	else if(i==14){
		arr = malloc(8*sizeof(float));
		//Ribes Roges
		(*size) = 8;
		arr[0] = 1.7228;
		arr[1] = 41.2174;
		arr[2] = 1.7146;
		arr[3] = 41.2119;
		arr[4] = 1.7261;
		arr[5] = 41.2134;
		arr[6] = 1.7231;
		arr[7] = 41.217;
		(*porcentaje) = 2.7754 / 100;
	}
	else if(i==15){
		arr = malloc(8*sizeof(float));
		//Sant Joan
		(*size) = 8;
		arr[0] = 1.7106;
		arr[1] = 41.2245;
		arr[2] = 1.7163;
		arr[3] = 41.2189;
		arr[4] = 1.7238;
		arr[5] = 41.2213;
		arr[6] = 1.7149;
		arr[7] = 41.2272;
		(*porcentaje) = 20.7239 / 100;
	}
	else if(i==16){
		arr = malloc(10*sizeof(float));
		//Santa Maria
		(*size) = 10;
 		arr[0] = 1.6758;
		arr[1] = 41.2178;
		arr[2] = 1.6825; 
		arr[3] = 41.2212;
		arr[4] = 1.6849;
		arr[5] = 41.2185;
		arr[6] = 1.6847;
		arr[7] = 41.2163;
		arr[8] = 1.6797;
		arr[9] = 41.2119;
		(*porcentaje) = 1.0868 / 100;
	}
	else if(i==17){
		//Tacó
		(*size) = 8;
		arr = malloc(8*sizeof(float));
		arr[0] = 1.7252;
		arr[1] = 41.2363;
		arr[2] = 1.7285;
		arr[3] = 41.2366;
		arr[4] = 1.7297;
		arr[5] = 41.2339;
		arr[6] = 1.7258;
		arr[7] = 41.2333;
		(*porcentaje) = 1.5749 / 100;
	}
	return arr;
}


float arreglaHora (float hora){

	float horaReturn = hora;

	int aux = hora;

	float parteDecimal = hora - aux;

	if(parteDecimal > 0.59){
		aux += 1;
		parteDecimal = fmod(parteDecimal,0.59);
		horaReturn = aux + parteDecimal;
	}

	return floorf(horaReturn * 100) / 100;

}


void main(int argc, char **argv){

	printf("Se va a generar un archivo de rutas reales. Por favor, introduzca el rango de edad que quieres simular (si quieres simular su totalidad indica 0 como edad inicial y 100 como final) \n");
	printf("A partir de que edad quieres comenzar la simulacion? \n");
	int iniEdad,finEdad;
	scanf("%d", &iniEdad);
	printf("Que edad quieres que sea el limite? \n");
	scanf("%d", &finEdad);
	printf("Has elegido como iniedad %d y %d como fin edad \n",iniEdad,finEdad	);

    FILE *file = fopen("edad_numPersonas.txt", "r"); // //Total Personas segun la edad https://www.idescat.cat/pub/?id=pmh&n=1180&geo=mun:083073&lang=es --> 65972 

	int numPersonasPorEdad[finEdad-iniEdad+1];

    int i=iniEdad;
    int num;

	int totalHabitantes = 65972;
	int totalBarrios = 18;
	int divisionParaIgualar = (65972-64783)/totalBarrios; //Le sumamos lo que queda a cada uno para igualar informaciones, sino la suma se descuadra


    while(fscanf(file, "%d", &num) > 0 && i >= iniEdad && i <= finEdad) {
        numPersonasPorEdad[i-iniEdad] = num;
        i++;
    }

    fclose(file);

	printf("Ejecutando...\n");

	for(int barr = 0; barr < totalBarrios; ++barr){
//  Para todas las edades
		int size;
		float porcentaje;
		float * coordsBarrio = retorna_coordenadas_barrio(barr,&porcentaje, &size);
		int contX = 0;
		int contY = 0;
		printf("Size coords: %ld\n", size);
		float coordenadasX[size/2];
		float coordenadasY[size/2];
		for(int q = 0; q < size; ++q){
			if(q%2==0){ 
				coordenadasX[contX] = coordsBarrio[q];
				++contX;
				printf("CoordX: %f", coordsBarrio[q]);
			}	else{	
				coordenadasY[contY] = coordsBarrio[q];
				++contY;
				printf("CoordY: %f\n", coordsBarrio[q]);
			}
		}
		for(int edad = iniEdad; edad < finEdad + 1; ++edad){
		//	printf("------------------------------------------\n");
		//	printf("Edad: %d\n",edad);	
		//	printf("------------------------------------------\n");
			//Para la cantidad de cada edad
			omp_set_num_threads(16);
			int valorAcomparar = (numPersonasPorEdad[edad] * porcentaje);
			#pragma omp parallel for 
			for(int persona = 0; persona < valorAcomparar; ++persona){
				int nThread = omp_get_thread_num();
				char horariosPers [20];
				sprintf(horariosPers, "hor%d", nThread);
				FILE *horarios = fopen(horariosPers, "a");
				//Generacion de casa
				int esta_dentro = 0;
				float casaX;
				float casaY;
				while(esta_dentro == 0){
					casaX = float_rand(1.64,1.76);
					casaY = float_rand(41.0,41.4);
					esta_dentro = esta_dentro_barrio (sizeof(coordenadasY)/sizeof(float), coordenadasX, coordenadasY, casaX, casaY);
				}

			//	if(barr==6){
			//		printf("Casa generada: %f,%f\n", casaY, casaX);
			//	}				
				//Generacion de trabajo/lugar de estudios
				
				float coordenadasSegundoPaso [2];				

				int random;

				float horaPrimerPaso;
				float horaSegundoPaso;
				float horaTercerPaso;
				float horaCuartoPaso;

				char tipo[30];

				if(edad<=21){ //estudiante
					//random = rand() % 36;
					random = 0;
					coordenadasSegundoPaso[0] = coordenadasCentrosEducativos[random][0];
					coordenadasSegundoPaso[1] = coordenadasCentrosEducativos[random][1];
					double distanciaPrimerPaso = distance(casaY,casaX,coordenadasSegundoPaso[1],coordenadasSegundoPaso[0],'K') * 1000;
					double tiempoArestar = distanciaPrimerPaso / 6000 ;
					horaPrimerPaso = arreglaHora(horarioCentrosEducativos[random][0] - tiempoArestar);
					horaSegundoPaso = horarioCentrosEducativos[random][1];
					horaTercerPaso = arreglaHora(horarioCentrosEducativos[random][1] + hora_aleatoria(1,2));
					horaCuartoPaso = arreglaHora(horaTercerPaso + float_rand(2,3));
					sprintf(tipo,"Estudiante ");
					//printf("Horario establecido para el estudiante es %f %f %f %f\n", horaPrimerPaso, horaSegundoPaso, horaTercerPaso, horaCuartoPaso);
				}
				else if ((tasaParo * valorAcomparar) > persona || edad >= 67){ //en el paro o jubilado
					//int randPasoPersonaEnParo = rand() % 7;
					int randPasoPersonaEnParo = 0;
					coordenadasSegundoPaso[0] = coordenadasLudico[randPasoPersonaEnParo][0];
					coordenadasSegundoPaso[1] = coordenadasLudico[randPasoPersonaEnParo][1];
					horaPrimerPaso = hora_aleatoria(7,8);
					horaSegundoPaso = hora_aleatoria(14,15);
					horaTercerPaso = arreglaHora(horaSegundoPaso + hora_aleatoria(2,3));
					horaCuartoPaso = arreglaHora(horaTercerPaso + hora_aleatoria(2,3));
					sprintf(tipo,"Paro/Jub ");
					//printf("Horario establecido para el paro/jubilado es %f %f %f %f\n", horaPrimerPaso, horaSegundoPaso, horaTercerPaso, horaCuartoPaso);
				}
				else{ //trabajador
					//random = rand() % 40;	
					random = 0;
					coordenadasSegundoPaso[0] = coordenadasCentrosTrabajo[random][0];
					coordenadasSegundoPaso[1] = coordenadasCentrosTrabajo[random][1];
					double distanciaPrimerPaso = distance(casaY,casaX,coordenadasSegundoPaso[1],coordenadasSegundoPaso[0],'K') * 1000;
					double tiempoArestar = distanciaPrimerPaso / 6000 ;
					horaPrimerPaso = arreglaHora(horarioLugaresTrabajo[random][0] - tiempoArestar);
					horaSegundoPaso = horarioLugaresTrabajo[random][1];
					horaTercerPaso = arreglaHora(horarioLugaresTrabajo[random][1] + hora_aleatoria(1,2));
					horaCuartoPaso = arreglaHora(horaTercerPaso + hora_aleatoria(1,2));
					sprintf(tipo,"Trabajador ");
					//printf("Horario establecido para el trabajador es %f %f %f %f\n", horaPrimerPaso, horaSegundoPaso, horaTercerPaso, horaCuartoPaso);
				}

				
				int randLudica = rand() % 7;

				float zonaLudica [2];
				zonaLudica[0] = coordenadasLudico[randLudica][0];
				zonaLudica[1] = coordenadasLudico[randLudica][1];

			//	printf("Coordenadas casa %lf,%lf. Coordenadas centro %lf,%lf. Zona ludica %lf,%lf \n", casaX, casaY, coordenadasSegundoPaso[0], coordenadasSegundoPaso[1], zonaLudica[0], zonaLudica[1]);
		
				
				char coordCasaX[30];
				sprintf(coordCasaX,"%f",casaX);
				char coordCasaY[30];
				sprintf(coordCasaY,"%f",casaY);

				char instX[30];
				char instY[30];
				sprintf(instX,"%f",coordenadasSegundoPaso[0]);
				sprintf(instY,"%f",coordenadasSegundoPaso[1]);

				char coordLudicaX[30];
				sprintf(coordLudicaX,"%f",zonaLudica[0]);
				char coordLudicaY[30];
				sprintf(coordLudicaY,"%f",zonaLudica[1]);




				char horaPrimerPasoChar[20];
				char horaSegundoPasoChar[20];
				char horaTercerPasoChar[20];
				char horaCuartoPasoChar[20];


				sprintf(horaPrimerPasoChar,"%.2f", horaPrimerPaso);
				sprintf(horaSegundoPasoChar,"%.2f", horaSegundoPaso);
				sprintf(horaTercerPasoChar,"%.2f", horaTercerPaso);
				sprintf(horaCuartoPasoChar,"%.2f", horaCuartoPaso);


				//------------------------------------------------------------------------------------------------------------
				//***************************************

				// PETICION CON TODOS LOS PASOS

				//***************************************



				//escribimos en fichero horarios coordenadas de la casa y horario del centro a donde tiene que ir
		
				//fprintf(horarios,"%s",tipo);
				/*fprintf(horarios,"%s %s %.2f ",coordCasaX, coordCasaY, horaPrimerPaso);
				fprintf(horarios,"%s %s %.2f ",instX, instY, horaSegundoPaso); 
				fprintf(horarios,"%s %s %.2f ",coordCasaX, coordCasaY, horaTercerPaso); //suponemos que cada uno tarda 1h en comer
				fprintf(horarios,"%s %s %.2f\n", coordLudicaX , coordLudicaY, horaCuartoPaso); //suponemos que cada uno esta 2h en cada sitio de zona ludica*/

				fclose(horarios);

				char nombreFichero [10];

				sprintf(nombreFichero,"File%d",nThread);
				

				char nombreFicheroTemp [10];

				strcpy(nombreFicheroTemp, "temp");
				strcat(nombreFicheroTemp, nombreFichero);
	
				int pid1 = fork();
				if(pid1 == 0){ 
					char* args[19];
					args[0] = "";
					args[1] = nombreFichero;
					args[2] = coordCasaX;
					args[3] = coordCasaY;
					args[4] = instX;
					args[5] = instY;
					args[6] = coordCasaX;
					args[7] = coordCasaY;
					args[8] = coordLudicaX;
					args[9] = coordLudicaY;
					args[10] = nombreFicheroTemp;
					args[11] = coordCasaX;
					args[12] = coordCasaY;
					args[13] = horariosPers;
					args[14] = horaPrimerPasoChar;
					args[15] = horaSegundoPasoChar;
					args[16] = horaTercerPasoChar;
					args[17] = horaCuartoPasoChar;
					args[18] = NULL;
					char * comando = "./genera_ruta.sh";
					execvp(comando, args); //TODO: PASARLE ARGUMENTOS CON EL EXECVP
					exit(-1);
				}
				int status1;
				waitpid(pid1,&status1,0);
			}

		}
		printf("Barrio %d completado...\n", barr+1);
	}

	//unifica docuementos generados en paralelo

	printf("Voy a unificar los documentos...\n");

	int finDocus = 0;
	int contadorFichero = 0;
	while(!finDocus){
		char nombreFicheroRutas [20];
		char nombreFicheroHorarios [20];
		sprintf(nombreFicheroRutas, "File%d", contadorFichero);
		sprintf(nombreFicheroHorarios, "hor%d", contadorFichero);
		//printf("Voy a unificar el documento File%d y hor%d\n", contadorFichero, contadorFichero);
		if( access( nombreFicheroRutas, F_OK ) != -1 ) { //compruebo uno de los dos ficheros ya que si uno existe, existe el otro
			int pid = fork();
			if(pid==0){
				char *args[] = {"./une_ficheros.sh", nombreFicheroRutas, nombreFicheroHorarios, NULL};
				execvp(args[0],args);
				exit(-1);
			}
			int status1;
			waitpid(pid,&status1,0);
			++contadorFichero;
		} else {
			printf("Voy a eliminar los ficheros temporales generados...\n");
			finDocus = 1;// fichero no existe, significa que ya hemos copiado todos
			int pid = fork();
			if(pid==0){
				char *args[] = {"./delete_temporals.sh", NULL};
				execvp(args[0],args);
				exit(-1);
			}
			int status1;
			waitpid(pid,&status1,0);
		}
		
	}

  	printf(ANSI_COLOR_GREEN   "GENERACIÓN DE RUTAS Y HORARIOS GPS COMPLETADA"   ANSI_COLOR_RESET "\n");

}
































