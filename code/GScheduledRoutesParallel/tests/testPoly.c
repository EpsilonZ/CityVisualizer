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



float float_rand( float min, float max )
{
    float scale = rand() / (float) RAND_MAX; /* [0, 1.0] */
    return min + scale * ( max - min );      /* [min, max] */
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


int main(){

	float *arr = malloc(10*sizeof(float));
	//La Collada - Els Sis Camins


	arr[0] = 1.7037;
	arr[1] = 41.2202;

	arr[2] = 1.7096;
	arr[3] = 41.224;

	arr[4] = 1.7076; 
	arr[5] = 41.2259;

	arr[6] = 1.7025;
	arr[7] = 41.2254;

	arr[8] = 1.7005;
	arr[9] = 41.2228; 


	float coordenadasX[10];
	float coordenadasY[10];



	coordenadasX[0] = 1.7037;
	coordenadasY[0] = 41.2202;


	coordenadasX[1] = 1.7096;
	coordenadasY[1] = 41.224;


	coordenadasX[2] = 1.7076;
	coordenadasY[2] = 41.2259;


	coordenadasX[3] = 1.7025;
	coordenadasY[3] = 41.2254;

	coordenadasX[4] = 1.6973;
	coordenadasY[4] = 41.2284;

	coordenadasX[5] = 1.6913;
	coordenadasY[5] = 41.2302;

	coordenadasX[6] = 1.6916;
	coordenadasY[6] = 41.2259;

	coordenadasX[7] = 1.6934;
	coordenadasY[7] = 41.2233;

	coordenadasX[8] = 1.6963;
	coordenadasY[8] = 41.2206;

	coordenadasX[9] = 1.7005; // ultimo
	coordenadasY[9] = 41.2228;


	int res;


	float casaX = 1.7002;
	float casaY = 41.2249;

	int esta_dentro;

	esta_dentro = esta_dentro_barrio (sizeof(coordenadasY)/sizeof(float), coordenadasX, coordenadasY, casaX, casaY);

	printf("Esta dentro %d\n", esta_dentro);

	for(int i = 0; i < 1000; i++){
		esta_dentro = 0;

		while(esta_dentro == 0){
			casaX = float_rand(1.64,1.76);
			casaY = float_rand(41.0,41.4);
			esta_dentro = esta_dentro_barrio (sizeof(coordenadasY)/sizeof(float), coordenadasX, coordenadasY, casaX, casaY);
		}
		printf("Casa generada: %f,%f\n", casaY, casaX);		
	}
}
