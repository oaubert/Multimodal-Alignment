var dataSpeech;
var dataLink;

function afficherParagraphe(n)
{
	var link = dataLink[n-1];
	var paragraphe = $(".data_paragraphe[data-id=\"" + link.dataset.idparagraphe + "\"]");

	$("#similarite" + n).html(link.dataset.similarite);
	$("#matching_words" + n).html(link.innerHTML);
	$("#texte" + n).html(paragraphe.html());

	$("#paragraphe" + n).on("click", function()
										{
											idSpeech = idSpeech +1; 

											if(idSpeech >= nbSpeech)
											{
												alert("fini");
											}
											else
											{
												afficherTranscript(idSpeech);
											}
										});
}

function afficherTranscript(id)
{
	dataSpeech = d3.selectAll(".data_speech[data-id=\"" + id + "\"]")[0];
	dataLink = d3.selectAll(".data_link[data-idspeech=\"" + id + "\"]")[0];

	$("#moyenne").html(dataSpeech[0].dataset.moyenne);
	$("#ecart_type").html(dataSpeech[0].dataset.ecart_type);
	$("#zero").html(dataSpeech[0].dataset.zero);
	$("#text_transcript").html(dataSpeech[0].innerHTML);

	afficherParagraphe(1);
	afficherParagraphe(2);
	afficherParagraphe(3);
}
