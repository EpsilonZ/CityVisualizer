define(['streamsaver'], function() {

	return {

		greet: function(rutasProjectPoints){


			console.log("voy a escribir el fichero")
			const fileStream = streamSaver.createWriteStream('rutas_simples_traducidas.txt')
			const writer = fileStream.getWriter()
			const encoder = new TextEncoder

			//console.log(rutasProjectPoints)
			var lineaAescribir = ""
			for(var i=0; i<rutasProjectPoints.length; ++i){
				//console.log(rutasProjectPoints[i].length)
				for(var q=0; q<rutasProjectPoints[i].length; ++q){
				//	console.log(q)
					var puntoAX = rutasProjectPoints[i][q][0]
					var puntoAY = rutasProjectPoints[i][q][1]
				//	console.log(puntoAX,puntoAY)
					lineaAescribir += (puntoAX.toString() + " " + puntoAY.toString() + " ")
				}
				
				writer.write(encoder.encode(lineaAescribir + "\n"))
				lineaAescribir=""
			}

			writer.close()

		}
	};
});
