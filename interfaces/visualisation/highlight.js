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

function highlightLink(id)
{
	if(!opacity)
	{
		d3.select(id).attr("stroke", color.fort);
	}
}

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

function highlightWord(lemme)
{
	$(".keyword[data-lemme=\"" + lemme + "\"]").css("color", "red");
	$(".matchingWords[data-lemme=\"" + lemme + "\"]").css("color", "red");
}

function unhighlightWord(lemme)
{
	$(".keyword[data-lemme=\"" + lemme + "\"]").css("color", "black");
	$(".matchingWords[data-lemme=\"" + lemme + "\"]").css("color", "black");
}
