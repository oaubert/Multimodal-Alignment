/*** Fonctions d'affichage de l'interface d'évaluation ***/

/** Cette interface affiche le transcript de la vidéo d'un coté, et les trois meilleurs paragraphes correspondant de l'autre
	Il est alors demandé de cliquer sur le paragraphe que l'on considère le plus proche du transcript

	On peut ainsi évaluer les résultats.
	Cette interface ne prend cependant pas en compte la possibilité que le paragraphe idéal ne fait pas parti des trois meilleurs affichés.
**/

var dataSpeech; //Variable globale stockant les données du speech actuel
var dataLink;	//Variable globale stockant les données des liens correspondant au speech actuel
var res = {}	//Variable globale stockant les résultats de l'évaluation

/* Affiche le n-ème meilleur paragraphe correspondant au speech actuel, avec plusieurs informations
	-La similarité entre le paragraphe et le speech
	-Les matching words
	-Le texte du paragraphe
*/
function afficherParagraphe(n)
{
	var link = dataLink[n-1];
	var paragraphe = $(".data_paragraphe[data-id=\"" + link.dataset.idparagraphe + "\"]");

	$("#similarite" + n).html(link.dataset.similarite);
	$("#matching_words" + n).html(link.innerHTML);
	$("#texte" + n).html(paragraphe.html());
}

/* Fonction activée lors d'un clic sur un paragraphe
	Ajoute le paragraphe dans les résultats comme étant le paragraphe le plus similaire au speech actuel
	Si le speech actuel n'est pas le dernier : Passe au speech suivant et actualise l'affichage
	Sinon : affiche les résultats
*/
function selectParagraphe(numero)
{
	res[idSpeech] = numero;

	if(idSpeech + 1 >= nbSpeech)
	{
		afficherResultat();
	}
	else
	{
		idSpeech = idSpeech + 1; 

		afficherTranscript(idSpeech);
	}
}

/* Actualise l'affichage
	-Affiche le transcript du speech actuel
	-Affiche les trois meilleurs paragraphes correspondant au speech actuel
*/
function afficherTranscript(id)
{
	dataSpeech = d3.selectAll(".data_speech[data-id=\"" + id + "\"]")[0];
	dataLink = d3.selectAll(".data_link[data-idspeech=\"" + id + "\"]")[0];

	$("#transcript_id").html(dataSpeech[0].dataset.id);
	$("#moyenne").html(dataSpeech[0].dataset.moyenne);
	$("#ecart_type").html(dataSpeech[0].dataset.ecart_type);
	$("#zero").html(dataSpeech[0].dataset.zero);
	$("#text_transcript").html(dataSpeech[0].innerHTML);

	afficherParagraphe(1);
	afficherParagraphe(2);
	afficherParagraphe(3);
}

/* Affiche les résultats */
function afficherResultat()
{
	string = "Résultat\n"

	for(i in res)
	{
		string += "Transcript " + i + " : Paragraphe " + res[i] + "\n";
	}

	alert(string);
}

/* Reset l'évaluation */
function resetEvaluation()
{
	res = {};
	idSpeech = 0;
	afficherTranscript(idSpeech);
}
