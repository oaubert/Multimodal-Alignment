/*** Gère l'affichage de l'interface d'évaluation ***/

/** Cette interface affiche speech par speech les trois meilleurs paragraphes correspondant.
	On sélectionne ensuite pour chaque paragraphe si il correspond ou pas, avant de passer au speech suivant.

	Cela permet une première évaluation des résultats.
	Elle ne prend cependant pas en compte le fait que les paragraphes peuvent correspondre au speech, sans être les meilleurs résultats possibles.
**/

var dataSpeech; 	//Variable globale contenant les données sur le speech actuel
var dataLink;		//Variable globale contenant les données sur les liens correspondant au speech actuel
var res = {};		//Variable globale contenant le résultat de l'évaluation
var idSpeech = 0;	//Variable globale contenant l'id du speech actuel

/* Affiche les informations du n-ème meilleur paragraphe
	-La similarité dans la baliseSimilarite
	-Le texte du paragraphe dans la baliseTexte
*/
function afficherParagraphe(n, baliseSimilarite, baliseTexte)
{
	var link = dataLink[n];
	document.getElementById(baliseSimilarite).innerHTML = link.dataset.similarite;

	var paragraphe = $(".data_paragraphe[data-id=\"" + link.dataset.idparagraphe + "\"]");

	document.getElementById(baliseTexte).innerHTML = paragraphe.html();	
}


/* Affiche l'interface pour le slide actuel
	-Vérifie que le slide est correct, sinon redirige vers la page fini.php
	-Vérifie que les radio button ne sont pas déjà coché
	-Sélectionne les données du speech actuel et des liens correspondants
	-Affiche les trois meilleurs paragraphes
	-Initialise la vidéo
*/
function afficher()
{
	if(idSpeech >= nbSpeech)
	{
		location.href="fini.php";
	}

	$("input[type='radio']").prop("checked", false);

	dataSpeech = d3.selectAll(".data_speech[data-id=\"" + idSpeech + "\"]")[0];
	dataLink = d3.selectAll(".data_link[data-idspeech=\"" + idSpeech + "\"]")[0];

	var debut = dataSpeech[0].dataset.begin;
	var fin = dataSpeech[0].dataset.end;

	afficherParagraphe(0, "similarite1", "texte1");
	afficherParagraphe(1, "similarite2", "texte2");
	afficherParagraphe(2, "similarite3", "texte3");

	initialisation(debut, fin);
}

/* Enregistre l'évaluation du speech actuel et passe au suivant */
function resultat()
{
	res[idSpeech] = {"1" : document.getElementById('p1_Oui').checked, "2" : document.getElementById('p2_Oui').checked, "3" : document.getElementById('p3_Oui').checked};

	idSpeech = idSpeech + 1;

	afficher();
}

/* Remet à zéro l'évaluation */
function resetEvaluation()
{
	res = {};

	idSpeech = 0;

	afficher();
}
