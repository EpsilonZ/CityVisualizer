var velocidadActual;

var rutas = [];


function enviaCalculado(socket,linePath){

	socket = io.connect("http://localhost:3000/", {
		reconnection: true
	});

	socket.on('connect', function () {



	for(var linea = 0; linea < 1000 ;++linea){	
		var lineaAenviar = [];
		for(var contadorTween = 0; contadorTween < 15716; ++contadorTween){
			var p = linePath[contadorTween].node().getPointAtLength(linea);
			var X = p.x;
			var Y = p.y;
			var punto = [X,Y];
	 	//	console.log(contadorTween,p.x,p.y);
			var envio = contadorTween + " " + X + " " + Y;
			lineaAenviar.push(envio);
			//matriz[linea][contadorTween] = punto;
		}
		socket.emit('infoEvent', lineaAenviar);
	}

		console.log("info enviada");
	});

}


function iniConexion(socket){

	//var io = require('socket.io-client');

	socket = io.connect("http://localhost:3000/", {
		reconnection: true
	});

	var horaActual = new Date(2018,1,10,7,0,0,0);
	velocidadActual = 1;

	socket.on('connect', function () {
		setInterval(function(){
		horaActual.setSeconds(horaActual.getSeconds() + velocidadActual*10);
		}, 1000);
		socket.emit('conectionEvent', velocidadActual);
		console.log('connected to localhost:3000');
		socket.on('clientEvent', function (data) {
			rutas = data;
		    console.log('message from the server:', data);
		    socket.emit('serverEvent', "Mensaje del cliente: thanks server! hora actual: " + horaActual);
		});
	});

	return socket;

}

function dameRutas(){
	return rutas;
}

function setSpeed(nuevaVelocidad){
	velocidadActual = nuevaVelocidad;
}

function textFileToArray( filename )
{
    var reader = (window.XMLHttpRequest != null )
        ? new XMLHttpRequest()
        : new ActiveXObject("Microsoft.XMLHTTP");
    reader.open("GET", filename, false );
    reader.send( );
    return reader.responseText.split(/(\r\n|\n)/g);
}

function get_rutas(rutasSimuladas,nombreFichero){

	var rutas1 = textFileToArray(nombreFichero);
	console.log(rutas1.length)
//	console.log(rutas1)
	//var rutas2 = textFileToArray("rutasTOTALES.txt");
	var cont = 0;
	var rutasbuenas=[];
	for(var j = 0; j < rutasSimuladas*2; j+=2){
		var rutaprueba=[];
		//console.log(j)	
		var tratarRutas = rutas1[j].split(',');
		for(var i = 0; i < tratarRutas.length; ++cont){
		    if(i==0){
				//console.log(j);
		        var coordx = tratarRutas[i].substring(2);
		        var coordy = tratarRutas[i+1].split("]")[0];
		        var coords = [coordx,coordy];
		        rutaprueba.push(coords);
		        //       console.log(rutaprueba);
		        i+=2;
		    }
		    else if (i != 0 && i < tratarRutas.length -2){
		        var coordauxx = tratarRutas[i].substring(1);
		        var coordauxy = tratarRutas[i+1].split("]")[0];
		        var coordaux = [coordauxx,coordauxy];
		        rutaprueba.push(coordaux);
		        i+=2;
		    }
		    else{
		        var coordauxxfin = tratarRutas[i].substring(1);
		        var coordauxyfin = tratarRutas[i+1].split("]]")[0];
		        var coordauxfin = [coordauxxfin,coordauxyfin];
		        rutaprueba.push(coordauxfin);
		        i+=2;
		    }
		}
		//console.log(j);
		//console.log(rutaprueba);
		rutasbuenas.push(rutaprueba);
	}

	return rutasbuenas;
}

function getRutasCalculadas(){

	//var rutas = textFileToArray("/home/epsilon/CitySimulation/nodejsServerClient/LogTotalFiltrado.txt");
	var rutas = textFileToArray("logTotalPasos.txt");
	var finRutas = 0;
	var cont = 0;
	var rutasTotales = [];
	
	rutas = rutas[0].split('||');

	for(var i = 0; i < rutas.length; i++){
		rutas[i] = rutas[i].split(' ');
		if(i!=0) rutas[i].shift();
	}
	console.log(rutas);
	console.log(rutas.length);
	

	return rutas;
	
}	


function escribeLogs(logCalculado){


	var fichero = new File (logCalculado, 'ficheroFiltrado.txt', {type: "text/plain;charset=utf-8"})
	FileSaver.saveAs(fichero)

}













