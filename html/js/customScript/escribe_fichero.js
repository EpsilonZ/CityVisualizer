define(['streamsaver'], function() {

	return {

		greet: function(rutasPath,length, rutasbuenas,opcion){

			const fileStream = streamSaver.createWriteStream('ficheroFiltrado.txt')
			const writer = fileStream.getWriter()
			const encoder = new TextEncoder

			var factorPuntosEscritos = 200

			for(var i = 0; i < length; ++i){
				
				var lineaAescribir = [];

				var longitud = rutasPath[i].node().getTotalLength() + 1;

				var longRutasBuenas = rutasbuenas[i].length
		
				var frecEscritura = longitud / factorPuntosEscritos

				var puntosEncontrados = 0

				var contEscritos = 0

				var ultimoPunto = 0
				
				for(var puntos = 0; puntos < longitud; ++puntos){

					var escrito = 0
					var p=0
						
					if(puntos == 0){
						p = rutasPath[i].node().getPointAtLength(0);
						lineaAescribir += (p.x + " " + p.y + " ")
						escrito = 1
						++puntosEncontrados
						ultimoPunto = p;
					}
		
					else if(puntos >= longitud - 1){
						p = rutasPath[i].node().getPointAtLength(longitud+1);
						lineaAescribir += (p.x + " " + p.y)
						escrito = 1
						++puntosEncontrados
						ultimoPunto = p
					}

					else if(longRutasBuenas > puntosEncontrados && escrito==0 && Math.abs(ultimoPunto.x - rutasbuenas[i][puntosEncontrados][0]) < 4  &&  Math.abs(ultimoPunto.y - rutasbuenas[i]		[puntosEncontrados][1]) < 4) {

						p = rutasPath[i].node().getPointAtLength(puntos);
						if( rutasbuenas[i][puntosEncontrados][0] ==p.x && rutasbuenas[i][puntosEncontrados][1]==p.y || 
							Math.abs(rutasbuenas[i][puntosEncontrados][0]-p.x ) < 4 && Math.abs(rutasbuenas[i][puntosEncontrados][1] - p.y) < 4 ){
							lineaAescribir += (p.x + " " + p.y + " ")
							++puntosEncontrados;
							escrito = 1
							ultimoPunto=p
						}	
					}

				    else if (contEscritos > frecEscritura && escrito == 0){
						contEscritos = 0
						if(p==0)
							p = rutasPath[i].node().getPointAtLength(puntos);
						lineaAescribir += (p.x + " " + p.y + " ")
						ultimoPunto=p
					}
				
					else if (escrito==0){ 
						++contEscritos
					}
			
				}
		
				writer.write(encoder.encode(lineaAescribir + "\n"))

			}

			writer.close()
		}
	};
});
