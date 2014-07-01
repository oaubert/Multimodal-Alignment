var svg = d3.select("#visualisation")
		    .append("svg")
		    .attr("width", window.innerWidth)
		    .attr("height", 200)
		    .style("border", "1px solid black")

	var isModeOpacity = false;

	var posTimeline = {"x" : 20, "y" : 20, "width" : window.innerWidth-40, "height" : 50}

	var color = {"faible" : "#FDE7E7", "moyen" : "#FAC5C5", "fort" : "red"}
	var colorParagraphe = {"nulle" : "transparent", "faible" : "#bbb", "moyen" : "#777", "fort" : "#444"}

	var timeline = svg.append("rect")
                         .attr("x", posTimeline.x)
                         .attr("y", posTimeline.y)
                         .attr("width", posTimeline.width)
                         .attr("height", posTimeline.height)
						 .attr("fill", "blue"); 

	
	var dataPage_traite = new Array()

		var largeurPage = (svg.attr("width") / dataPage.length) - 10
		
		for(i = 0; i < dataPage.length; i++)
		{
			var d = dataPage[i];

			dataPage_traite[i] = {'id' : d.id, "number" : d.dataset.id, "src" : chemin + "img/PICTURE_" + d.dataset.numero + ".jpg", "x" : i*(largeurPage + 10), "y" : 200, "width" : largeurPage, "height" : d.dataset.hauteur * (largeurPage / d.dataset.largeur)}

			if(svg.attr("height") < dataPage_traite[i].y + dataPage_traite[i].height)
			{
				svg.attr("height", dataPage_traite[i].y + dataPage_traite[i].height)
			}
		}


    var imgs = svg.selectAll("image")
        .data(dataPage_traite)
		.enter()
			.append("svg:image")
			.attr('x',function(d){return d.x;})
			.attr('y',function(d){return d.y;})
			.attr('width', function(d){return d.width;})
			.attr('height', function(d){return d.height;})
			.attr("xlink:href",function(d){return d.src;});


	var dataParagraphe_traite = new Array()
		
		for(i = 0; i < dataParagraphe.length; i++)
		{
			var d = dataParagraphe[i];
			var point = new Array()
			
			point[0] = getPoint(dataPage_traite[d.dataset.idpage], d.dataset.left, d.dataset.top)
			point[1] = getPoint(dataPage_traite[d.dataset.idpage], (100 - d.dataset.right), d.dataset.top)
			point[2] = getPoint(dataPage_traite[d.dataset.idpage], (100 - d.dataset.right), (100 - d.dataset.bottom))
			point[3] = getPoint(dataPage_traite[d.dataset.idpage], d.dataset.left, (100 - d.dataset.bottom))

			dataParagraphe_traite[i] = {'id' : d.id, "page" : d.dataset.idPage, "point" : point, "number" : d.dataset.id}
		}
	


	var speech = createSpeech();

	var paragraphe = createParagraphe();
	
	var link = createLink();

	var opacity;
	
	modeLine();

	selectLink(document.getElementById('nbLink').value, document.getElementById('seuil').value);


function createSpeech()
{
	var speech = svg.selectAll(".speech")
						.data(dataSpeech)
						.enter()
							.append("rect")
								.attr("class", "speech")
								.attr("id", function(d){return "svg_" + d.id;})
								.attr("data-id", function(d){return d.dataset.id;})
								.attr("x", function(d){return coordonneeTimeline(d.dataset.begin);})
				                .attr("y", posTimeline.y)
				                .attr("width", function(d){return (coordonneeTimeline(d.dataset.end) - coordonneeTimeline(d.dataset.begin));})
				                .attr("height", posTimeline.height)
								.attr("fill", "grey")
								.attr("data-selected", "false")
								.attr("stroke", "red")
								.on("mouseover", function(d)
												 {
													highlightSpeech("#" + $(this).attr("id"));
							
													highlightTriplet({"data-idspeech" : $(this).attr("data-id")});

													$("#highligh").text($("#" + d.id).text());
												 })
								.on("mouseout", function(d)
												 {
													unhighlightTriplet();
													$("#highligh").text("");
												 })
								.on("click", function(d)
												{
													if($(this).attr("data-selected") == "true")
													{
														unselectTriplet();
													}
													else
													{
														unselectTriplet();
														selectTriplet({"data-idspeech" : $(this).attr("data-id")});
													}
												});

	return speech;

}


function createParagraphe()
{
	var paragraphe = svg.selectAll(".paragraphe")
							.data(dataParagraphe_traite)
							.enter()
								.append("polygon")
								.attr("class", "paragraphe")
								.attr("id", function(d){return "svg_" + d.id;})
								.attr("data-id", function(d){return d.number;})
								.attr("data-selected", "false")
								.attr("points", function(d)
													{
														var res = "";
														for(i = 0; i < 4; i++)
														{
															res = [res, [d.point[i].x, d.point[i].y].join(",")].join(" ");
														}
														
														return res; 
													})
								.attr("stroke-width", 1)
								.attr("stroke", "green")
								.attr("fill", "#fff")/*function(d)
												{
													return getColorParagraphe(d.id);
												})*/
								.attr("fill-opacity", 0.5)
								.on("mouseover", function(d)
												 {
													highlightParagraphe("#" +  $(this).attr("id"));

													highlightTriplet({"data-idparagraphe" : $(this).attr("data-id")});

													$("#highligh").text($("#" + d.id).text());
												 })
								.on("mouseout", function(d)
												 {
													unhighlightTriplet();
													$("#highligh").text("");
												 });

	return paragraphe;
}



function createLink()
{
	var link = svg.selectAll(".link")
					.data(dataLink)
					.enter()
						.append("line")
						.attr("class", "link")
						.attr("id", function(d){return "svg_" + d.id;})
						.attr("data-id", function(d){return d.id;})
						.attr("data-idspeech", function(d){return d.dataset.idspeech;})
						.attr("data-idparagraphe", function(d){return d.dataset.idparagraphe;})
						.attr("data-similarite", function(d){return d.dataset.similarite;})
						.attr("data-affiche", "off")
						.attr("data-selected", "false")
						.attr("x1", function(d)
									{
										var s = dataSpeech[d.dataset.idspeech];

										return center(coordonneeTimeline(s.dataset.begin), coordonneeTimeline(s.dataset.end));
									})
						.attr("y1", center(posTimeline.y, posTimeline.y + posTimeline.height))
						.attr("x2", function(d)
									{
										var p = dataParagraphe_traite[d.dataset.idparagraphe].point;

										return center(p[0].x, p[1].x);
									})
						.attr("y2", function(d)
									{
										var p = dataParagraphe_traite[d.dataset.idparagraphe].point;

										return center(p[0].y, p[3].y);
									})

						.attr("stroke-width", 2)
	                    .attr("stroke", color.faible)
						.style("display", "none")
						.on("mouseover", function(d)
										 {
											highlightLink("#" +  $(this).attr("id"));

											highlightTriplet({"id" : $(this).attr("id")});
										 })
						.on("mouseout", function(d)
										 {
											unhighlightTriplet();
										 });

	return link;
}



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

	highlightTriplet({"data-selected" : "true"});
}



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

	if(!opacity)
		afficheLink();	
}

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

	$(".keyword").on("click", function(){selectKeyword(this);});
	$(".matchingWords").on("click", function(){selectMatchingWord(this);});
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
	}
}

function unhighlightTriplet()
{
	if(opacity)
	{
		$(".paragraphe[data-selected!=\"true\"]").attr("fill-opacity", 0.1);
		$(".speech[data-selected!=\"true\"]").attr("fill-opacity", 0.1);
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
	


function coordonneeTimeline(time)
{
	return posTimeline.x + time*posTimeline.width / dureeSpeech;
}


function center(a, b)
{
	return (a + b) / 2;
}

function getPoint(page, pourcentX, pourcentY)
{
	var x = page.x + pourcentX*page.width/100;
	var y = page.y + pourcentY*page.height/100;

	return {"x" : x, "y" : y};
}

function similarity2color (similarity) {
   // Convert a [0..1] value into a color between 0xddd and 0x777
   //return "#" + Math.floor((0x777 + (0xddd - 0x777) * (1 - .1))).toString(16);

	if($w[1] > 15)
		$color = "#777";
	else if($w[1] > 10)
		$color = "#999";
	else if($w[1] > 5)
		$color = "#bbb";
	else if($w[1] > 0)
		$color = "#ddd";
	else
		$color = "#eee";
}


function getColorParagraphe(id)
{
	links = searchLinksOfParagraphe(id);

	if(links.length == 0)
	{
		return colorParagraphe.nulle;
	}
	else if(links.length < 3)
	{
		return colorParagraphe.faible;
	}
	else if(links.length < 6)
	{
		return colorParagraphe.moyen;

	}
	else
	{
		return colorParagraphe.fort;
	}
}
