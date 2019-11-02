

//Inicializa variables de ejecucion
var index = 0
var linea = 0
var lineasAdded = 0
var indiceActual = 0
var contLineaVisualizar = 0
var offsetTotal=0
var offsetSizes = 0
var velocidad = 0

//hora inicial de simulacion 
var horaReferencia = new Date(2018,1,10,6,0,0,0);

//Numero de habitantes a visualizar
//var numPoints = 1185
var numPoints = 68726

//Size del canvas donde proyectaremos la visualizacion
var width=1700
var height=940

//Variable donde cargaremos los sizes de las lineas a cargar
var sizes;

var zoomDiff = 0

//
var center = []
var zoom = 14
var traducedCenter = []

//Size inicial de los puntos que visualizaremos
var pointWidth=4
var pointMargin=4

//Inicializamos todos los habitantes de la visualizacion 
var points=createPoints(numPoints,pointWidth,width,height)

//Escala de la visualizacion, por defecto a 1. En caso de querer establecer zoom esta escala variara
var screenScale=window.devicePixelRatio||1


//Creamos el canvas donde proyectaremos la visualizacion
canvas=d3.select("body").append("canvas")
	.attr("width",width*screenScale)
	.attr("height",height*screenScale)
	.style('position',"absolute")
	.style('left', 0 + "px")
	.style('top', 0 + "px")


function createPoints(numPoints,pointWidth,width,height) {
	var points=d3.range(numPoints).map(function(id){
		return{id:id,color:"blue"}});
	return points;
}


function empieza_simulacion(file) {

	nombreBase = file.name
	ficheroSizes= file.name+"-"+"sizes.txt"

	fetch('Data/'+ficheroSizes)
		.then(respuesta => respuesta.text())
		.then(texto => {	
			sizes = resuelveSizes(texto)
		});

	canvas.node().getContext("2d").scale(screenScale,screenScale),
	d3.select("body").append("div")
	.attr("class","play-control")
	.text("Empieza la simulación")
	.on("click",function(){parseFile(file,visualizaLinea),d3.select(this).style("display","none")});

}

function resuelveSizes(texto){

	//Nos cargamos el fichero sizes en un simple array para manejarlo de forma simple

	var aux = texto.split("\n")
	var numeros = []

	for(var i = 0; i < aux.length; ++i){
		numeros.push(parseInt(aux[i],10))
	}

	return numeros;
}


function probability(n) {
  return Math.random() <= n;
}

function draw(linea,lineaAtratar) {

	const ctx = canvas.node().getContext('2d');
	ctx.save();

	//Guardamos el size de los puntos (por tema de la interaccion con la interficie)
	widthActual = pointWidth
	heightActual = pointMargin

	//Eliminar contenido del canvas actual
	ctx.clearRect(0, 0, width, height);

	//Este indice lo utilizaremos para acceder a los atributos de las lineas que cargamos
	index=0

	var valueDiffOperation = 0
	if(zoomDiff != 0){
		if(zoomDiff < 0){
			valueDiffOperation = Math.abs(zoomDiff)*2; //each zoom multiplies *2 or /2 depending on zoom in or zoom out
		} else{
			valueDiffOperation = Math.abs(zoomDiff)/2;
		}
	}

	console.log("valuediffope", valueDiffOperation);

	var centerWhenDrawing = traducedCenter

	for (let i = 0; i < points.length; ++i) {
		//Obtenemos el habitante del array
		const point = points[i];

		//Obtenemos el color del mapa de calor del habitante, punto X del habitante, punto Y del habitante
		//A modo de recordatorio por cada habitante: PUNTOX1 PUNTOY1 COLOR1 PUNTOX2 PUNTOY2 COLOR2 ... PUNTOXN PUNTOYN COLORN

		//An answer from a google guy metersPerPx = 156543.03392 * Math.cos(latLng.lat() * Math.PI / 180) / Math.pow(2, zoom)

		var coordX = parseFloat(lineaAtratar[index])
		var coordY = parseFloat(lineaAtratar[index+1])

		if(zoomDiff < 0){
			var diffX = Math.abs(coordX - centerWhenDrawing[0]);
			var diffY = Math.abs(coordY - centerWhenDrawing[1]);
			if(coordX>centerWhenDrawing[0]){
				if(coordY>centerWhenDrawing[1]){
					if(valueDiffOperation==2){
						coordX = diffX + coordX + diffX * (valueDiffOperation - 2)
						coordY = diffY + coordY + diffY * (valueDiffOperation - 2)
					} else {
						coordX = diffX + coordX + diffX * (valueDiffOperation / 2)
						coordY = diffY + coordY + diffY * (valueDiffOperation / 2)
					}
				}
				else{
					if(valueDiffOperation==2){
						coordX = diffX + coordX + diffX * (valueDiffOperation - 2)
						coordY = coordY - diffY - diffY * (valueDiffOperation - 2)
					} else{
						coordX = diffX + coordX + diffX * (valueDiffOperation / 2)
						coordY = coordY - diffY - diffY * (valueDiffOperation / 2)
					}
				}
			}
			else{
				if(coordY>traducedCenter[1]){
					if(valueDiffOperation == 2){
						coordX = coordX - diffX - diffX * (valueDiffOperation - 2)
						coordY = diffY + coordY + diffY * (valueDiffOperation - 2)
					} else{
						coordX = coordX - diffX - diffX * (valueDiffOperation / 2)
						coordY = diffY + coordY + diffY * (valueDiffOperation / 2)
					}

					//coordX = Math.abs((Math.abs(coordX - traducedCenter[0])) - coordX - coordX * (valueDiffOperation - 2))
					//coordY = Math.abs((Math.abs(coordY - traducedCenter[1])) + coordY + coordY * (valueDiffOperation - 2))
				}
				else{
					if(valueDiffOperation == 2){
						coordX = coordX - diffX - diffX * (valueDiffOperation - 2)
						coordY = coordY - diffY - diffY * (valueDiffOperation - 2)
					} else{
						coordX = coordX - diffX - diffX * (valueDiffOperation / 2)
						coordY = coordY - diffY - diffY * (valueDiffOperation / 2)
					}

					//coordX = Math.abs((Math.abs(coordX - traducedCenter[0])) - coordX - coordX * (valueDiffOperation - 2))
					//coordY = Math.abs((Math.abs(coordY - traducedCenter[1])) - coordY - coordY * (valueDiffOperation - 2)) 
				}
			}
		}
	

		if (lineaAtratar[index+2] == "#FF0000"){
		 //   if(probability(0.25)){ //solo se representara el 25% de los puntos
					ctx.fillStyle = lineaAtratar[index+2];
					ctx.fillRect(coordX, coordY, widthActual, heightActual);
			//	}
			} 

		else if (lineaAtratar[index+2] == "#FF4000"){
		  //  if(probability(0.5)){ //solo se representara el 50% de los puntos
					ctx.fillStyle = lineaAtratar[index+2];
					ctx.fillRect(coordX, coordY, widthActual, heightActual);
				//}
			}

		else if (lineaAtratar[index+2] == "#FF8000"){
		  //  if(probability(0.75)){ //solo se representara el 75% de los puntos
					ctx.fillStyle = lineaAtratar[index+2];
					ctx.fillRect(coordX, coordY, widthActual, heightActual);
			//	}
			}

		else if (lineaAtratar[index+2] == "#FFBF00" && Math.random()*5 == 1){
		  //  if(probability(0.8)){ //solo se representara el 80% de los puntos
					ctx.fillStyle = lineaAtratar[index+2];
					ctx.fillRect(coordX, coordY, widthActual, heightActual);
			//	}

			} else{
				ctx.fillStyle = lineaAtratar[index+2];
				ctx.fillRect(coordX, coordY, widthActual, heightActual);
			}

			//Aumentamos el indice para el siguiente punto
			index+=3
		}

		//Restablecemos el canvas con los puntos actualizados
		ctx.restore();
}

function animate(lineaLeida) {

    // Guardamos la posicion de inicio del punto
    points.forEach(point => {
      point.sx = point.x;
      point.sy = point.y;
    });

	//Como actualizamos aumentamos la hora
	var h = horaReferencia.getHours();
	var m = horaReferencia.getMinutes();
	var s = horaReferencia.getSeconds() + 10
	horaReferencia.setSeconds(s)
	document.getElementById('3').innerHTML =
	h + ":" + m + ":" + s;
	
	//Dividimos la linea por espacios para obtener cada uno de los parametros de forma correcta
	var lineaAtratar = lineaLeida.split(" ")

	//Mandamos a pintar la linea	
    draw(linea,lineaAtratar);

	//Aumentamos la linea ya que ya ha sido pintada
	++linea
}


function checkTime(i) {
//Esta funcion tiene la simple utilidad de poner 0 detras de un numero en caso de ser < 9. Por ejemplo las 6:1 serian las 6:01

	if (i < 10) {i = "0" + i};  
	return i;
}

function parseFile(file, callback) {
	
	//Obtenemos el size del fichero a leer para tener una referencia de cuando debemos parar de leer
    var fileSize   = file.size;

	//Contador de lineas visualizadas
	contLineaVisualizar = 0

	//Size a cargarse en memoria a partir del fichero sizes con el indice de contador de linea
	var chunkSize = sizes[contLineaVisualizar]

	//Offset que nos indica por que parte del fichero estamos
    offsetSizes    = 0;

	//Referencia al propio objeto
    var self = this; 

	//Inicializamos a null el bloque de lectura
    var chunkReaderBlock = null;

	//Evento de lectura del fichero
    var readEventHandler = function(evt) {
        if (evt.target.error == null) {
			//Una vez hemos realizado la lectura, aumentamos el offset
            offsetSizes += chunkSize + 1;

			//Una vez hemos cargado la linea, la mandamos a la funcion callback (visualizaLinea)
            callback(evt.target.result); 
			
        } else {
			//Gestion del error en caso de fallo en cargarse en memoria la linea
            console.log("Read error: " + evt.target.error);
            return;
        }
        if (offsetSizes >= fileSize) {
			//Finalizamos la lectura del fichero
            return;
        }

		if(offsetTotal>0 || offsetTotal < 0){
			//Si la interficie nos dice que tenemos que aumentar o disminuir la hora
			offsetSizes = offsetTotal
			offsetTotal=0
			contLineaVisualizar = indiceActual
			indiceActual = 0
			linea+=lineasAdded
			lineasAdded = 0
		} else{
			//En caso de seguir el proseguir normal de la visualizacion, nos dirigimos a la siguiente linea
			if(velocidad==0) contLineaVisualizar = contLineaVisualizar + 1
            else{
				for(i=0;i<velocidad;++i){
					if(contLineaVisualizar < sizes.length - 1){
						contLineaVisualizar = contLineaVisualizar + 1
						offsetSizes+=sizes[contLineaVisualizar] + 1
						if (offsetSizes >= fileSize) {
							//Finalizamos la lectura del fichero
							return;
						}
						var s = horaReferencia.getSeconds() + 10
						horaReferencia.setSeconds(s)
					}
				}
				contLineaVisualizar+=1
			}		
		}


		//Cargamos la siguiente linea a visualizar
		chunkSize = sizes[contLineaVisualizar]
	
		//Mandamos a leer el siguiente bloque
	    chunkReaderBlock(offsetSizes, chunkSize, file);
    }

    chunkReaderBlock = function(_offsetSizes, length, _file) {
		//Creamos el objeto FileReader
        var r = new FileReader();
		
		//Genereamos un blob a partir de la lectura de la linea marcada por el chunk
        var blob = _file.slice(_offsetSizes, length + _offsetSizes);

		//Se lo pasamos al readEventHandler el cual mandara a la funcion callback a visualizar
        r.onload = readEventHandler;
        r.readAsText(blob);
    }

    // now let's start the read with the first block
    chunkReaderBlock(offsetSizes, chunkSize, file);
}

function visualizaLinea(contenido){

	//Mandamos a la funcion animate para viusalizar el contenido
	animate(contenido)
}

//A PARTIR DE AQUI SON FUNCIONES QUE GESTIONAN LA VISTA

function aumenta_size(){

	if(pointWidth < 10){
		pointWidth = pointWidth + 1
	}

	if(pointMargin < 10){
		pointMargin = pointMargin +1
	}
}

function disminuye_size(){

	if(pointWidth > 1){
		pointWidth = pointWidth - 1
	}

	if(pointMargin > 1){
		pointMargin = pointMargin - 1
	}
}

function aumenta_rapidez(){
	velocidad+=1
}

function disminuye_rapidez(){
	if(velocidad>0){
		velocidad-=1
	}
}

function avanza_tiempo(){
	

	indiceActual = contLineaVisualizar
	offsetTotal = offsetSizes
	lineasAdded = 0

	var segs = 0
	while (indiceActual < sizes.length && segs < 60) {
		offsetTotal += sizes[indiceActual] + 1
		lineasAdded += 1
		indiceActual+=1
		segs+=10
	}

	lineasAdded-=1

	var h = horaReferencia.getHours();
    var s = horaReferencia.getSeconds() + segs;
    horaReferencia.setSeconds(s);
    s = checkTime(s)
	//var m = horaReferencia.getMinutes() + minutos;
	//horaReferencia.setMinutes(m)
	//m = checkTime(m);
	document.getElementById('3').innerHTML =
	h + ":" + m;

	console.log(h,m)

}

function retrasa_tiempo() {

	indiceActual = contLineaVisualizar
	offsetTotal = offsetSizes
	lineasAdded = 0

	var segs = 0
	var ticks = 0

	while (indiceActual < sizes.length && indiceActual>1 && ticks < 60) {
		//console.log("voy a restar ", sizes[indiceActual])
		offsetTotal -= sizes[indiceActual-1] 
		lineasAdded -= 1
		indiceActual -= 1
		segs -= 10
		ticks+=1
	}

	offsetTotal-=ticks
	
	lineasAdded -= 1

	var h = horaReferencia.getHours();
	var s = horaReferencia.getSeconds() + segs;
	horaReferencia.setSeconds(s)
	s = checkTime(s);
	document.getElementById('3').innerHTML = h + ":" + m;

}

function initCenter (mapCenter, mapTraducedCenter){
	center = mapCenter;
	traducedCenter = [mapTraducedCenter.x,mapTraducedCenter.y];
	console.log("traduced center ", traducedCenter);
}

function initZoom (mapZoom) {
	zoom = mapZoom;
}

function zoomChanged(zoomLevel, newCenter, traducedCenter){
	console.log("zoom, zoomlevel", zoom, zoomLevel);
	zoomDiff = zoom - zoomLevel;
	console.log("zoomDiff ", zoomDiff);
	mapMoved(newCenter, traducedCenter);
}

function mapMoved(mapNewCenter, mapTraducedCenter){
	center = mapNewCenter;
	traducedCenter = [mapTraducedCenter.x,mapTraducedCenter.y];
	console.log("traduced center ", traducedCenter);
}


