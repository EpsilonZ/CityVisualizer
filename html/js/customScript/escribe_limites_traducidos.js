define(['filesaver'], function() {
	return {
		greet: function(limites){
			var file = new File([limites], "limitesCarreteraTraducidosVilanovaILaGeltru.txt", {type: "text/plain;charset=utf-8"});
			saveAs(file);
		}
	};
});
