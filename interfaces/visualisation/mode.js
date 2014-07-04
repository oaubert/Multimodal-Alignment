function changeMode()
{
	if(opacity)
		modeLine();
	else
		modeOpacity();
}

function modeLine()
{	
	svg.selectAll(".speech")
		.attr("stroke-opacity", 1.0)
		.attr("fill-opacity", 1.0);

	svg.selectAll(".paragraphe")
		.attr("stroke-opacity", 1.0)
		.attr("fill-opacity", 1.0);

	timeline.attr("stroke-opacity", 1.0);
	timeline.attr("fill-opacity", 1.0);

	opacity = false;

	afficheLink();

	$(".paragraphe").attr("fill", "#fff");

	highlightTriplet({"data-selected" : "true"});
}

function modeOpacity()
{
	$(".speech")
		.attr("fill", "grey")
		.attr("stroke-opacity", 0.1)
		.attr("fill-opacity", 0.1);

	$(".paragraphe")
		.attr("stroke", "green")
		.attr("stroke-opacity", 0.1)
		.attr("fill-opacity", 0.1);

	timeline.attr("stroke-opacity", 0.1);
	timeline.attr("fill-opacity", 0.1);

	opacity = true;

	$(".link").css("display", "none");

	$(".paragraphe").attr("fill", function(){return $(this).attr("data-color");});

	highlightTriplet({"data-selected" : "true"});
}
