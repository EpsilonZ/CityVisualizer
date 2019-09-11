define(['filesaver'], function() {
	return {
		greet: function(horarios){
			var file = new File([horarios], "horarios_traducidos.txt", {type: "text/plain;charset=utf-8"});
			saveAs(file);
		}
	};
});
