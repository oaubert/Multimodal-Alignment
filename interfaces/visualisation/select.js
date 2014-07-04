/*** Fonctions permettant la sélection des éléments visualisés ***/

/* 
	Il est possible de cliquer sur les speechs, ce qui sélectionnera le speech, ainsi que les liens les paragraphes correspondants
	Les informations sur ces liens s'afficheront en dessous de la visualisation :
		-À gauche, le texte du speech, avec les informations sur ses similarités (moyenne, écart-type et pourcentage de zéro)
		-Au milieu, les textes des paragraphes correspondant, avec leurs scores de similarité avec le speech, ainsi que la liste des matchingWords
		-Dans tous les textes, les mots ont des backgrounds de différentes couleurs :
			-Gris, si le mot est un stop words
			-Vert, si le mot est un mot significatif. La teinte de vert varie selon le tfidf du mot dans le document. Plus il est foncé, plus le tfidf est fort (voir colorTfidf dans utils.js)
		-Les mots peuvent être mis en valeur (voir highlightWord dans highlight.js), et sélectionnés, affichant différentes informations à droite :
			-Si c'est un mot du texte : le lemme, le df, l'idf, le tf et le tfidf
			-Si c'est un matchingWords : la similarité (produit scalaire)

	La sélection met aussi en valeur (voir highlight.js) les éléments sélectionnés, tant qu'ils seront sélectionnés, c'est-à-dire jusqu'à ce qu'on reclique sur le speech, ou qu'on en sélectionne un autre.
*/




/* Sélectionne tous les éléments acceptés par le filtre passé en paramètre (voir la fonction getTripet, dans utils.js)
	On pense aussi à ajouter les actions de clic et de passage de souris aux mots nouvellement affichés
*/
function selectTriplet(filtre)
{
	var triplets = getTriplet(filtre);
	var paragrapheHtml = document.getElementById("info_paragraphe");
	var speechHtml = document.getElementById("info_speech");

	paragrapheHtml.innerHTML = "";
	speechHtml.innerHTML = "";

	for(var i = 0; i < triplets.length; i++)
	{
		highlightParagraphe("#svg_" + triplets[i]["paragraphe"])
		highlightSpeech("#svg_" + triplets[i]["speech"])
		highlightLink("#svg_" + triplets[i]["link"])

		$("#svg_" + triplets[i]["paragraphe"]).attr("data-selected", "true");
		$("#svg_" + triplets[i]["speech"]).attr("data-selected", "true");
		$("#svg_" + triplets[i]["link"]).attr("data-selected", "true");

		if($("#info_" + triplets[i]["paragraphe"]).length == 0)
		{
			paragrapheHtml.innerHTML += selectParagraphe(triplets[i]["paragraphe"], triplets[i]["link"]);
		}

		if($("#info_" + triplets[i]["speech"]).length == 0)
		{
			speechHtml.innerHTML += selectSpeech(triplets[i]["speech"]);
		}
	}

	$(".keyword")
		.on("click", function(){selectKeyword(this);})
		.on("mouseover", function(){highlightWord($(this).attr('data-lemme'));})
		.on("mouseout", function(){unhighlightWord($(this).attr('data-lemme'));});
	$(".matchingWords")
		.on("click", function(){selectMatchingWord(this);})
		.on("mouseover", function(){highlightWord($(this).attr('data-lemme'));})
		.on("mouseout", function(){unhighlightWord($(this).attr('data-lemme'));});

	d3.selectAll(".keyword")
		.style("background-color", function(){return colorTfidf($(this).attr('data-tfidf'));});

}
 
/* Sélectionne un paragraphe, en précisant le contexte (le lien) pour les matchingWords et la similarité */
function selectParagraphe(idParagraphe, idLink)
{
	var string = "";
	var p = $("#" + idParagraphe);
	string += "<div id=\"info_" + idParagraphe + "\" >Paragraphe " + p.attr('data-id') + " - " + parseFloat($("#" + idLink).attr('data-similarite')).toFixed(4);
	string += "<div class=\"metadata\">Matching words : " + $("#" + idLink).html() + "</div>";
	string += "<div class=\"text\">" + p.html() + " </div></div>";

	return string;
}

/*Sélectionne un speech*/
function selectSpeech(idSpeech)
{
	var string = "";
	var s = $("#" + idSpeech);
	
	string += "<div id=\"info_" + idSpeech + "\" >Speech " + s.attr('data-id');
	string += "<div class=\"metadata\">"
	string += "<span class=\"moyenne\">Moyenne : " + parseFloat(s.attr('data-moyenne')).toFixed(4) + "</span><br/>";
	string += "<span class=\"ecart_type\">Écart type : " + parseFloat(s.attr('data-ecart_type')).toFixed(4) + "</span><br/>";
	string += "<span class=\"zero\">Pourcentage de zéro : " + parseFloat(s.attr('data-zero')).toFixed(4) + "</span><br/></div>";
	string += "<div class=\"text\">" + s.html() + "</div></div>";

	return string;
}


/* Sélectionne un mot*/
function selectKeyword(element)
{
	var string = "<div id=\"info_word\">" + $(element).text();
	string += "<div class=\"donnee\">";
	string += "<span class=\"metadata\" data-info=\"lemme\">Lemme : " + $(element).attr('data-lemme') + "</span><br />";
	string += "<span class=\"metadata\" data-info=\"df\">Df : " + $(element).attr('data-df') + "</span><br />";
	string += "<span class=\"metadata\" data-info=\"idf\">Idf : " + parseFloat($(element).attr('data-idf')).toFixed(4) + "</span><br />";
	string += "<span class=\"metadata\" data-info=\"tf\">Tf : " + $(element).attr('data-tf') + "</span><br />";
	string += "<span class=\"metadata\" data-info=\"tfidf\">Tfidf : " + parseFloat($(element).attr('data-tfidf')).toFixed(4) + "</span></div></div>";

	$("#highligh").html(string);
}

/* Sélectionne un matching word */
function selectMatchingWord(element)
{
	var string = "<div id=\"info_matchingWord\">" + $(element).text();
	string += "<div class=\"donnee\">";
	string += "<span class=\"metadata\" data-info=\"value\">Similarite (produit scalaire) : " + parseFloat($(element).attr('data-value')).toFixed(4) + "</span></div></div>";

	$("#highligh").html(string);
}

/* Désélectionne tous les éléments sélectionnés */
function unselectTriplet()
{
	$(".paragraphe[data-selected=\"true\"]").attr("data-selected", "false");
	$(".speech[data-selected=\"true\"]").attr("data-selected", "false");
	$(".link[data-selected=\"true\"]").attr("data-selected", "false");
	unhighlightTriplet();

	$("#info_paragraphe").text("");
	$("#info_speech").text("");
}
