define(['streamsaver'], function() {
	return {
		greet: function(rutas,horarios){

			console.log(horarios)

			var index=0;

			var velocidad = 100;

			var linea=0;

			var indices = []

			var horaReferencia = new Date(2018,1,10,6,0,0,0);

			var colores = [];

			//var numPoints = rutas.length - 2

			var numPoints = 10

			var contEscribir = 0

			var cuentaIntervalos = 0
	
			var numeroFichero = 1

			var formatoFichero = ".txt"

			var nombreFichero = numeroFichero.toString() + formatoFichero

			for (var i = 0; i < numPoints; ++i) indices.push(0)


			function reply_click(number){

				velocidad=number;
			}

			function draw(linea) {
			  const ctx = canvas.node().getContext('2d');
			  ctx.save();

			  // erase what is on the canvas currently
			  ctx.clearRect(0, 0, width, height);

			  // draw each point as a rectangle
			  for (let i = 0; i < points.length; ++i) {
				const point = points[i];
				//console.log(colores[linea][i]);
			   // ctx.fillStyle = colores[linea][i];
				ctx.fillStyle = "blue";
				ctx.fillRect(point.x, point.y, pointWidth, pointWidth);
			  }

			  ctx.restore();
			}


			function animate(layout) {

			  require(['config'],function() {

		      fileStream = streamSaver.createWriteStream(nombreFichero)
		      writer = fileStream.getWriter()
		      encoder = new TextEncoder 

			  var intervalo = setInterval(function(){

				++cuentaIntervalos

				console.log(cuentaIntervalos)

				if(cuentaIntervalos >= 500){
					
					numeroFichero = numeroFichero + 1
					nombreFichero = numeroFichero.toString() + formatoFichero
					cuentaIntervalos = 0
					writer.close()
					fileStream = streamSaver.createWriteStream(nombreFichero)
					writer = fileStream.getWriter()
				
				}

				var s = 0
				var h = horaReferencia.getHours();
				var m = horaReferencia.getMinutes() + 1;
				horaReferencia.setMinutes(m) 
				document.getElementById('3').innerHTML =
				h + ":" + m;

				var acabados = []

			    var lineaEscrita = []

				if(h == 0 || h == 1 || h == 2 || h == 3 || h == 4 ) h+=24

				points.forEach(point => {
		
				  ++contEscribir;

				  if(index==0) contAcabados = 0

				  if(lineasAtratar[index].length > indices[index]){ //Si aun quedan puntos de la ruta

					if(linea == 0){ //Si es la primera vuelta para todos
				   		 point.x = lineasAtratar[index][indices[index]];
						 point.y = lineasAtratar[index][indices[index]+1];
						 lineaEscrita += (point.x + " " + point.y);
						 if(index + 1 < numPoints) lineaEscrita += " "
						// console.log(point.x,point.y)
					}

					else if (horarios[index].length == 0){ //si ya no queda horario
						point.x = lineasAtratar[index][indices[index]];
					 	point.y = lineasAtratar[index][indices[index]+1];
						indices[index] += 2
						lineaEscrita += (point.x + " " + point.y);
						if(index + 1 < numPoints) lineaEscrita += " "
						//console.log(point.x,point.y)
					}


					else if (horarios[index].length == 4){
						
						var horaSalida = (horarios[index][0][2] + "").split(".");
						var hora = horaSalida[0]
						var minutos = horaSalida[1]

						if(h>=hora || (h==hora && m>=minutos) || h==hora && m==minutos){
				   			 point.x = lineasAtratar[index][indices[index]];
						 	 point.y = lineasAtratar[index][indices[index]+1];
							 lineaEscrita += (point.x + " " + point.y);
							 if(index + 1 < numPoints) lineaEscrita += " "	
							 //console.log(point.x,point.y)
						  	 indices[index] += 2
							 horarios[index].shift()
						}
						else{
				   			 point.x = lineasAtratar[index][indices[index]];
						 	 point.y = lineasAtratar[index][indices[index]+1];
							 lineaEscrita += (point.x + " " + point.y);
							 if(index + 1 < numPoints) lineaEscrita += " "	
							// console.log(point.x,point.y)

						}
			
					}

					else if (lineasAtratar[index][indices[index]] == horarios[index][0][0] && lineasAtratar[index][indices[index]+1] == horarios[index][0][1] || 
					 		Math.abs(lineasAtratar[index][indices[index]] - horarios[index][0][0]) < 6 && Math.abs(lineasAtratar[index][indices[index]+1] - horarios[index][0][1]) < 6 ){ //si es el 								paso a donde va en horario	

						var horasAux = (horarios[index][0][2] + "").split(".");
						var hora = horasAux[0]
						var minutos = horasAux[1]

						/*if( lineasAtratar[index].length > indices[index] + 1 && 
							(Math.abs(lineasAtratar[index][indices[index]] - horarios[index][0][0]) + Math.abs(lineasAtratar[index][indices[index]+1] - horarios[index][0][1])) >
				 			(Math.abs(lineasAtratar[index][indices[index] + 2] - horarios[index][0][0]) + Math.abs(lineasAtratar[index][indices[index] + 3] - horarios[index][0][1])) ){

							point.x = lineasAtratar[index][indices[index]];
						 	point.y = lineasAtratar[index][indices[index]+1]; //si el siguiente punto esta mas cerca del destino
							lineaEscrita += (point.x + " " + point.y);
							if(index + 1 < numPoints) lineaEscrita += " "
							indices[index] += 2

						}*/

						if(h >= hora || (h == hora && m >= minutos)) {

							// Si le toca salir respentando el horario 	 
				   			 point.x = lineasAtratar[index][indices[index]];
						 	 point.y = lineasAtratar[index][indices[index]+1];
							 lineaEscrita += (point.x + " " + point.y);
							 if(index + 1 < numPoints) lineaEscrita += " "	
							 //console.log(point.x,point.y)
						  	 indices[index] += 2
							 horarios[index].shift()
						}

						else{ // Si le toca respetar el horario no aumentamos el indice, por tanto no puede actualizar
				   			 point.x = lineasAtratar[index][indices[index]];
						 	 point.y = lineasAtratar[index][indices[index]+1];
							 lineaEscrita += (point.x + " " + point.y);
							 if(index + 1 < numPoints) lineaEscrita += " "	
							// console.log(point.x,point.y)
						}

					 } else{
						//console.log("actualiza")
						point.x = lineasAtratar[index][indices[index]];
					 	point.y = lineasAtratar[index][indices[index]+1];
						lineaEscrita += (point.x + " " + point.y);
						if(index + 1 < numPoints) lineaEscrita += " "
						//console.log(point.x,point.y)
						indices[index] += 2
					 }
	
		
				  } else{
				  		lineaEscrita += (lineasAtratar[index][indices[index]-2] + " " + lineasAtratar[index][indices[index]-1]);
						if(index + 1 < numPoints) lineaEscrita += " "
						++contAcabados;
				  }

				  ++index;

				  if(index==numPoints && contAcabados==numPoints){
					 clearInterval(intervalo)
					 console.log("fin de simulacion")
					 writer.close()
				  }

				  else if (index == numPoints) {
					lineaEscrita += "\n"
				    writer.write(encoder.encode(lineaEscrita));
				  }

				});
				++linea;
				index=0
			 	}, velocidad);

				});
			}


			var width=792-654+1000
			var height=695-471+1000
			var pointWidth=4
			var pointMargin=3
			var currLayout=0
			var points=createPoints(numPoints,pointWidth,width,height)
			var screenScale=window.devicePixelRatio||1


			canvas=d3.select("body").append("canvas")
				.attr("width",width*screenScale)
				.attr("height",height*screenScale)
				.style('position',"absolute")
				.style('left',"-10px")
				.style('top',"0px")


			var lineasAtratar = []


			for(var i = 0; i < numPoints; ++i){

				var aux = rutas[i].split(" ")

				//console.log(i)
			
				if(aux.length % 2 != 0) aux.pop()
	

				lineasAtratar.push(aux)		
	
			}


			canvas.node().getContext("2d").scale(screenScale,screenScale),
			d3.select("body").append("div")
			.attr("class","play-control")
			.text("Empieza la simulación")
			.on("click",function(){animate(),d3.select(this).style("display","none")});


			function checkTime(i) {
				if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
				return i;
			}


			function createPoints(numPoints,pointWidth,width,height) {
				var points=d3.range(numPoints).map(function(id){
					return{id:id,color:"blue"}});
				return points;
			}

		}
	};
});

