/*** Fonctions permettant la mise en valeur (highlight) des éléments visualisés ***/

/* La façon de mettre en valeur dépend du mode utilisé, Line ou Opacity*/


/* Met en valeur un paragraphe
	-mode Line : il est encadré en rouge (au lieu de vert)
	-mode Opacity : il passe à une opacité de 1, au lieu de 0.1
*/
function highlightParagraphe(id)
{
	if(opacity)
	{
		d3.select(id).attr("fill-opacity", 1.0);
		d3.select(id).attr("stroke-opacity", 1.0);
	}
	else
	{
		d3.select(id).attr("stroke", "red");
	}
}

/* Met en valeur un speech
	-mode Line : il devient plus foncé
	-mode Opacity : il passe à une opacité de 1, au lieu de 0.1
*/
function highlightSpeech(id)
{
	if(opacity)
	{
		d3.select(id).attr("fill-opacity", 1.0);
		d3.select(id).attr("stroke-opacity", 1.0);
	}
	else
	{
		d3.select(id).attr("fill", "#666666");
	}
}

/* Met en valeur un lien
	-mode Line : il devient plus foncé
	-mode Opacity : rien, les liens ne sont pas directement affichés dans ce mode
*/
function highlightLink(id)
{
	if(!opacity)
	{
		d3.select(id).attr("stroke", color.fort);
	}
}

/* Met en valeur tout les éléments accepté par le filtre passé en paramètre (voir la fonction getTripet, dans utils.js)*/
function highlightTriplet(filtre)
{
	triplets = getTriplet(filtre);

	for(var i = 0; i < triplets.length; i++)
	{
		highlightParagraphe("#svg_" + triplets[i]["paragraphe"])
		highlightSpeech("#svg_" + triplets[i]["speech"])
		highlightLink("#svg_" + triplets[i]["link"])

		if(opacity)
			d3.select("#svg_" + triplets[i]["paragraphe"]).attr("fill", function(){return similarity2color(d3.select("#svg_" + triplets[i]["link"]).attr("data-similarite"));});
	}
}

/* Enlève la mise en valeur de tous les éléments (qui ne sont pas sélectionnés, voir select.js)
*/
function unhighlightTriplet()
{
	if(opacity)
	{
		$(".paragraphe[data-selected!=\"true\"]").attr("fill-opacity", 0.1);
		$(".speech[data-selected!=\"true\"]").attr("fill-opacity", 0.1);
		$(".paragraphe[data-selected!=\"true\"]").attr("fill", $(this).attr("data-color"));
		$(".paragraphe[data-selected!=\"true\"]").attr("stroke-opacity", 0.1);
		$(".speech[data-selected!=\"true\"]").attr("stroke-opacity", 0.1);
	}
	else
	{
		$(".paragraphe[data-selected!=\"true\"]").attr("stroke", "green");
		$(".speech[data-selected!=\"true\"]").attr("fill","grey");
		$(".link[data-selected!=\"true\"]").attr("stroke", color.faible);
	}
}

/* Met en valeur un lemme
	-Lorsqu'on passe la souris sur un mot (voir select.js), on va mettre en valeur tous les mots qui ont le même lemme (et donc considérés comme les mêmes pour les mesures de similarité)
	-On met en valeur les mots dans les textes, mais aussi dans les listes de matchingWords
	-Le mot va devenir rouge, au lieu de noir
*/
function highlightWord(lemme)
{
	$(".keyword[data-lemme=\"" + lemme + "\"]").css("color", "red");
	$(".matchingWords[data-lemme=\"" + lemme + "\"]").css("color", "red");
}

/* Enlève la mise en valeur d'un lemme*/
function unhighlightWord(lemme)
{
	$(".keyword[data-lemme=\"" + lemme + "\"]").css("color", "black");
	$(".matchingWords[data-lemme=\"" + lemme + "\"]").css("color", "black");
}
