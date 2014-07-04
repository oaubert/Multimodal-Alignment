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

function selectParagraphe(idParagraphe, idLink)
{
	var string = "";
	var p = $("#" + idParagraphe);
	string += "<div id=\"info_" + idParagraphe + "\" >Paragraphe " + p.attr('data-id') + " - " + parseFloat($("#" + idLink).attr('data-similarite')).toFixed(4);
	string += "<div class=\"metadata\">Matching words : " + $("#" + idLink).html() + "</div>";
	string += "<div class=\"text\">" + p.html() + " </div></div>";

	return string;
}

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

function selectMatchingWord(element)
{
	var string = "<div id=\"info_matchingWord\">" + $(element).text();
	string += "<div class=\"donnee\">";
	string += "<span class=\"metadata\" data-info=\"value\">Similarite (produit scalaire) : " + parseFloat($(element).attr('data-value')).toFixed(4) + "</span></div></div>";

	$("#highligh").html(string);
}

function unselectTriplet()
{
	$(".paragraphe[data-selected=\"true\"]").attr("data-selected", "false");
	$(".speech[data-selected=\"true\"]").attr("data-selected", "false");
	$(".link[data-selected=\"true\"]").attr("data-selected", "false");
	unhighlightTriplet();

	$("#info_paragraphe").text("");
	$("#info_speech").text("");
}
