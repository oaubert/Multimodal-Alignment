var dataSpeech;
var dataLink;
var res = {}

function afficherParagraphe(n)
{
	var link = dataLink[n-1];
	var paragraphe = $(".data_paragraphe[data-id=\"" + link.dataset.idparagraphe + "\"]");

	$("#similarite" + n).html(link.dataset.similarite);
	$("#matching_words" + n).html(link.innerHTML);
	$("#texte" + n).html(paragraphe.html());
}

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


function afficherResultat()
{
	string = "Résultat\n"

	for(i in res)
	{
		string += "Transcript " + i + " : Paragraphe " + res[i] + "\n";
	}

	alert(string);
}
