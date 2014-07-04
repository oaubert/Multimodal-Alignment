function afficheLink()
{
	$(".link").css("display", "none");

	$(".link[data-affiche=\"on\"]")
		.css("display", "inline");

}



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

function similarity2color (similarity) {
   // Convert a [0..1] value into a color between 0xddd and 0x777
	s = Math.floor((0x77 + (0xdd - 0x77) * (1 - similarity))).toString(16);
 	return "#" + s + s + s;

	//return "#" + Math.floor(1911 + (3549 - 1911) * (1-similarity)).toString(16);

	/*var color;

	if(similarity > 15)
		color = "#777";
	else if(similarity > 10)
		color = "#999";
	else if(similarity > 5)
		color = "#bbb";
	else if(similarity > 0)
		color = "#ddd";
	else
		color = "#eee";

	return color;*/
}
