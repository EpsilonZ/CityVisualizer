


var horarios = [];

var rutas = [];

fetch('Data/horarios_filtrados.txt')
	.then(response => response.text())
	.then(text => horarios=resuelveHorarios(text))


fetch('Data/ficheroFiltrado.txt')
	.then(respuesta => respuesta.text())
	.then(texto => {
		var fichero = new File([texto], {type: "text/plain"})
		parseFile(fichero,imprimeContenido)
	});



function resuelveRutas(texto){

	var rutasAux = []
	
	var auxRutas = texto.split("\n")

	var longitud = auxRutas.length

	for(var i = 0; i < longitud; ++i){
		
		rutasAux[i] = []

		var lineaRuta = auxRutas[i].split(" ")

		for (var j = 0; j < lineaRuta.length; j+=2){

			rutasAux[i].push([lineaRuta[j],lineaRuta[j+1]])

		}
		
		rutasAux[i].pop();
	
	}

	rutasAux.pop();

	return rutasAux;

}


function resuelveHorarios(text){
		
	var horas = new Array()

	var aux = text.split("\n")
	
	for(var i = 0; i < aux.length; ++i){
				
		horas[i] = new Array()

		var linea = aux[i].split(" ")
		var sum = 0
		var coordAux = [];

		for(var j = 0; j < linea.length; j+=3){

			horas[i].push([linea[j],linea[j+1],linea[j+2]])

		}

	}

	horas.pop()

	return horas
}

function parseFile(file, callback) {
    var fileSize   = file.size;
    var chunkSize  = 64 * 1024; 
    var offset     = 0;
    var self       = this; 
    var chunkReaderBlock = null;

    var readEventHandler = function(evt) {
        if (evt.target.error == null) {
            offset += evt.target.result.length;
            callback(evt.target.result); 
        } else {
            console.log("Read error: " + evt.target.error);
            return;
        }
        if (offset >= fileSize) {
			rutas = rutas.split("\n")
			//console.log(rutas[1])
            console.log("Done reading file");
			require(['customScript/escribe_logTotal'], function (a){ 
					a.greet(rutas,horarios);
			});
            return;
        }
        chunkReaderBlock(offset, chunkSize, file);
    }

    chunkReaderBlock = function(_offset, length, _file) {
        var r = new FileReader();
        var blob = _file.slice(_offset, length + _offset);
        r.onload = readEventHandler;
        r.readAsText(blob);
    }
    chunkReaderBlock(offset, chunkSize, file);
}


function imprimeContenido(contenido){
	rutas += contenido
}





