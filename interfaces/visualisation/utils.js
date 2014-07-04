/*** Fonctions utiles ***/

/* Affiche les liens sélectionné d'après les seuils (voir selectLink) */
function afficheLink()
{
	$(".link").css("display", "none");

	$(".link[data-affiche=\"on\"]")
		.css("display", "inline");

}

/* Sélectionne les liens d'après les seuils saisies avec des slides (voir visualisation.php, la div contrôle) 
	Seul ces liens seront affichés par afficheLink et seront pris en compte lors de la mise en valeur et de la sélection des éléments (voir highlight.js et select.js)
*/
function selectLink(nbLink, seuil)
{
	$(".link").attr("data-affiche", "off");

	for(i = 0; i < nbSpeech; i++)
	{
		$(".link[data-idspeech=\"" + i + "\"]:lt(" + nbLink + ")")
			.filter(function(){
				return parseFloat($(this).data("similarite")) >= seuil;})
			.attr("data-affiche", "on");
	}

	$(".paragraphe").attr("data-color", function(){return similarity2color(moyenneSimilarite($(this).attr("data-id")));});

	if(!opacity)
		afficheLink();
	else
		$(".paragraphe").attr("fill", function(){return $(this).attr("data-color");});
}


/* Renvoie tous les éléments qui valide le filtre passé en paramètre
	Le filtre est un dictionnaire de la forme attribut : valeur, et s'applique sur les liens
	On va garder tous les liens affichable (voir selectLink) dont les attributs donnés dans le filtre ont la bonne valeur associée, et ont renverra tous ces liens, avec leurs speechs et paragraphes correspondant
*/
function getTriplet(filtre)
{
	var links = $(".link[data-affiche=\"on\"]")
					.filter(function(){
								var res = true;
								for(i in filtre)
								{
									if($(this).attr(i) != filtre[i])
									{
										res = false;
									}
								}

								return res;
							});

	var triplets = []

	for(var l = 0; l < links.length; l++)
	{
		triplets.push({"speech" : "speech_" + $(links[l]).attr('data-idspeech'), "paragraphe" : "paragraphe_" + $(links[l]).attr('data-idparagraphe'), "link" : $(links[l]).attr("data-id")});
	}

	return triplets
}


/* Calcule la moyenne de similarité d'un paragraphe avec tous les speechs auquel il est relié (pour les liens sélectionné, voir selectLink) */
function moyenneSimilarite(idParagraphe)
{
	var links = $(".link[data-affiche=\"on\"][data-idparagraphe=\"" + idParagraphe + "\"]");
	var somme = 0.0;

	for(var l = 0; l < links.length; l++)
	{
		somme += $(links[l]).attr("data-similarity");
	}

	if(links.length == 0)
		return 0.0;
	else
		return somme/links.length;
}

/* Renvoie une couleur (plus ou moins foncée) selon la valeur de tfidf d'un mot
	On utilise une échelle allant de zéro au tfidf maximum de tous les mots de tous les documents
	La plupart des tfidfs sont très faible, et très peu sont dans la moitié supérieure, on a donc une échelle progressive
*/
function colorTfidf(value)
{
	var part = tfidf_max/10;
	var find = false;
	var i = 1;
	var res;

	if(value == 0.0)
		return "#fff";
	else if(value <= 1.0*part)
		return "#bfb";
	else if(value <= 2.0*part)
		return "#9d9";
	else if(value <= 3.0*part)
		return "#7b7";
	else if(value <= 5.0*part)
		return "#595";
	else if(value <= 7.0*part)
		return "#373";
	else if(value <= 10.0*part)
		return "#151";
	else
		return "#000";

}


/* Renvoie une couleur selon la valeur de similarité correspondante 
	L'échelle va de 0 à 1
*/
function similarity2color (similarity) {
   // Convert a [0..1] value into a color between 0xddd and 0x777
	s = Math.floor((0x77 + (0xdd - 0x77) * (1 - similarity))).toString(16);
 	return "#" + s + s + s;
}
