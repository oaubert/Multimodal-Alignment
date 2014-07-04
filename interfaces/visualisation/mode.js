/*** Fonctions permettant de changer de mode de visualisation ***/

/* Il existe deux modes possibles pour visualiser les liens entre les speechs et les paragraphes :
	-mode Line : Les liens sont affichés en dur, sous la forme de lignes reliant les éléments
	-mode Opacity : Les éléments ont une opacité faible, et les liens sont visualisés indirectement, par la mise en valeur des éléments liés entre eux (voir highlight.js)
*/


/* Passe au mode actuellement non sélectionné */
function changeMode()
{
	if(opacity)
		modeLine();
	else
		modeOpacity();
}

/* Passe au mode Line 
	-Remet tous les éléments à une opacité de 1
	-Affiche les liens
*/
function modeLine()
{	
	svg.selectAll(".speech")
		.attr("stroke-opacity", 1.0)
		.attr("fill-opacity", 1.0);

	svg.selectAll(".paragraphe")
		.attr("stroke-opacity", 1.0)
		.attr("fill-opacity", 1.0);

	timeline.attr("stroke-opacity", 1.0);
	timeline.attr("fill-opacity", 1.0);

	opacity = false;

	afficheLink();

	$(".paragraphe").attr("fill", "#fff");

	highlightTriplet({"data-selected" : "true"});
}

/* Passe au mode Opacity
	-Met tous les éléments à une opacité de 0.1
	-Cache les liens
	-Dans ce mode, les paragraphes ont une couleur de remplissage de plus en plus foncés selon leurs similarités avec les speechs (voir similarity2color dans utils.js)
*/
function modeOpacity()
{
	$(".speech")
		.attr("fill", "grey")
		.attr("stroke-opacity", 0.1)
		.attr("fill-opacity", 0.1);

	$(".paragraphe")
		.attr("stroke", "green")
		.attr("stroke-opacity", 0.1)
		.attr("fill-opacity", 0.1);

	timeline.attr("stroke-opacity", 0.1);
	timeline.attr("fill-opacity", 0.1);

	opacity = true;

	$(".link").css("display", "none");

	$(".paragraphe").attr("fill", function(){return $(this).attr("data-color");});

	highlightTriplet({"data-selected" : "true"});
}
