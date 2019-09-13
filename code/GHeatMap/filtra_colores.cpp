#include <iostream>
#include <fstream>
#include <string>
#include <math.h>
#include <vector>
#include <iterator>
#include <sstream>
#include <algorithm>
#include <utility>      
using namespace std;


const std::string red("\033[0;31m");
const std::string reset("\033[0m");



//Colores que se usan
//pagina utilizada https://html-color-codes.info/codigos-de-colores-hexadecimales/
//#00FFFF --> azul flojo
//#00FFBF --> verde flojo
//#00FF80 --> verde mas fuerte
//#00FF40 --> verde mas fuerte
//#00FF00 --> verde mas fuerte
//#FFFF00 --> amarillo
//#FFBF00 --> naranja
//#FF8000 --> naranja mas oscuro
//#FF4000 --> rojo
//#FF0000 --> granate

//TODO: El size del devuelveLIneaParseada peta en algun sitio a causa del size, o vuelvo a lo de antes donde lo hago todo de una cogiendo de dos en dos o arreglo este problema

vector<string> arrayColores = {"#00FFFF","#00FFBF","#00FF80","#00FF40","#00FF00","#FFFF00","#FFBF00","#FF8000","#FF4000","#FF0000"};


string retornaColor (int cantidad){

	string retorno;
	
	if (cantidad == 1) retorno = arrayColores[0];
	else if (cantidad < 10) retorno = arrayColores[1];
	else if (cantidad < 20) retorno = arrayColores[2];
	else if (cantidad < 30) retorno = arrayColores[3];
	else if (cantidad < 40) retorno = arrayColores[4];
	else if (cantidad < 50) retorno = arrayColores[5];
	else if (cantidad < 70) retorno = arrayColores[6];
	else if (cantidad < 100) retorno = arrayColores[7];
	else if (cantidad < 200) retorno = arrayColores[8];
	else retorno = arrayColores[9];

	return retorno;

}


bool primerosPuntos = false;

vector <float> devuelveLineaParseada ( string linea ){

	vector <float> vectorRetorno;

	//cout<<linea<<endl;

	string aux;
	int contador = 0;

	for(int iterador = 0; iterador< linea.size(); ++iterador){

	//	cout<<linea[iterador]<<endl;
		if(linea[iterador] != ' '){
			aux.push_back(linea[iterador]);
		}
		else{
			if(aux.size() > 0){
				++contador;
			//	cout<<"Contenido de aux: "<<aux<<endl;
				float auxFloat = stof(aux.c_str());
				vectorRetorno.push_back(auxFloat);
				aux.clear();
			}
		}
	}

	if(!aux.empty()){
		float auxFloat = stof(aux.c_str());
		vectorRetorno.push_back(auxFloat); //el ultimo que no contiene espacio al final
	}

//	cout<<vectorRetorno.size()/2<<endl;

	return vectorRetorno;
}

int main(int argc, char *argv[]) {


	if(argc > 3 || argc < 3){

		cout<<red<<"HA OCURRIDO UN ERROR"<<reset<<endl;
		cout<<"----------------------------------------------------------"<<endl;
		cout<<"El número de argumentos es el incorrecto. Para ejecutar correctamente el generador de mapa de calor dinámico tendrás que especificar el fichero que contiene la traza generada"; 
		cout<<"y en segundo lugar el nombre del fichero al cual quieres escribirlo (cuidado, si ese fichero se escribirá encima del contenido)."<<endl;
		cout<<"----------------------------------------------------------"<<endl;
		cout<<"Usage: ./filtra_colores ficheroTraza ficheroDestino"<<endl;

	}


	string line;

	ofstream fichero;
	fichero.open (argv[2]);
	//  fichero << "Writing this to a file.\n"; --> Escribimos contenido

	ifstream ficheroSource (argv[1]);

	//dividimos en secciones el cuadrado de la simulacion

	float topLeftx = 654;
	float topLefty = 471;

	float bottomRightx = 792;
	float bottomRighty = 695;

	float left = -10; //desplazamiento de este cuadrado de simulacion en x
	float top = -4; //desplazamiento de este cuadrado de simulacion en y

	float posicionLeftxReal = left;
	float posicionLeftyReal = top;

	float posicionRightxReal = bottomRightx - topLeftx + 1000 + left;
	float posicionRightyReal = bottomRighty - topLefty + 1000 + top;

	float sizeDivision=10;

	float divisionesX = bottomRightx-topLeftx / sizeDivision;
	float divisionesY = bottomRighty-topLefty / sizeDivision;

	//inicializamos la matriz de arrays (tendremos en cada posicion un array "vacio", preparado para añadir cada posicion

	int contador = 0;

	int sizeLinea = 0;


	if (ficheroSource.is_open())
	{

		//leemos cada linea del fichero

		while ( getline (ficheroSource,line) )
		{

			vector<vector<vector<int> > > matrix(ceil(divisionesX));
			for ( int i = 0 ; i < ceil(divisionesX) ; i++ )
			   matrix[i].resize(ceil(divisionesY));
			//cout<<"aaa"<<endl;
			contador++;
			//cout << line << '\n'; //Cada linea del fichero de los logs
			
			cout<<contador<<endl;

			vector<float> linea = devuelveLineaParseada(line); 
		
			//if(contador==1) sizeLinea = linea.size()/2;
		//	cout<<sizeLinea<<endl;

	//		cout<<"Linea size: "<<linea.size()<<endl;

			//leemos cada xy de la línea y le asignamos la posicion en la matriz (si no esta no se apunta), apuntamos su numero de punto y sus coordenadas

			for(int contadorLinea = 0; contadorLinea < linea.size(); contadorLinea++){

				//cogemos la x y correspondientes
				float coordX = linea[contadorLinea];
				float coordY = linea[contadorLinea+1];

				//miramos si se encuentra dentro del margen de nuestro cuadro

				//si esta dentro lo apuntamos
				if (coordX >= posicionLeftxReal && coordX <= posicionRightxReal && coordY >= posicionLeftyReal && coordY <= posicionRightyReal){					

					int cuadradoX = coordX / sizeDivision;
					int cuadradoY = coordY / sizeDivision;

					matrix[cuadradoX][cuadradoY].push_back(contadorLinea/2);
				}
		

			}

			vector <string> colores (linea.size()/2); 
			 

			//le asignamos sin color a todos primero y luego sobrescrimos los que tienen
			for(int cont = 0; cont < linea.size()/2; ++cont){
				colores[cont] = "x";
			}			

			
			//contamos el numero de puntos en cada posicion y le asignamos el color
			//tambien podemos asignar el tamaño de cada circulo en funcion de los cercanos, asignamos "representante" de cada cuadrado, los demas indices el tamaño es x y color es x, es decir,
			//que no queremos que se pinten.

			for(int r = 0; r < divisionesX; ++r){
				for(int q = 0; q < divisionesY; ++q){
					int contador = 0;
					for(int t = 0; t < matrix[r][q].size(); ++t){	
						++contador;
						if(t==matrix[r][q].size()-1){ 
							for(int apunta = 0; apunta < matrix[r][q].size(); ++apunta){	
								colores[matrix[r][q][apunta]] = retornaColor(contador);
							}
						}
					}
				}
			}


			int cont=0;
			for(cont = 0; cont < linea.size()/2; ++cont){
				fichero << colores[cont]; 
				if(cont != sizeLinea - 1) fichero << " ";
			}
		
			fichero << endl;

			
		}

	ficheroSource.close();

	}

	else cout << "No he sido capaz de leer el fichero, revisa el path"<<endl; 



	fichero.close();

	
	 return 0;

}
