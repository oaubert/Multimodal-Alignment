/** Initialisation de la visualisation **/

//Création du svg
var svg = d3.select("#visualisation")
		    .append("svg")
		    .attr("width", window.innerWidth)
		    .attr("height", 200)
		    .style("border", "1px solid black")

	
	/* Création de 4 groupes à visualiser :
		-imageGroup : les images de l'article (une image par page)
		-speechGroup : la visualisation des speechs
		-paragrapheGroup : la visualisation des paragraphes
		-linkGroup : la visualisation des liens
	*/
	
	var imageGroup = svg.append("g").attr("id", "svg_group_image");
	var speechGroup = svg.append("g").attr("id", "svg_group_speech");
	var paragrapheGroup = svg.append("g").attr("id", "svg_group_paragraphe");
	var linkGroup = svg.append("g").attr("id", "svg_group_link");


	//Options

	var color = {"faible" : "#FDE7E7", "moyen" : "#FAC5C5", "fort" : "red"}
	var colorParagraphe = {"nulle" : "transparent", "faible" : "#bbb", "moyen" : "#777", "fort" : "#444"}

	var tfidf_max = Math.max($("#data_pdf").attr("data-tfidf_max"), $("#data_transcript").attr("data-tfidf_max"));


	//Création et affichage de la timeline de la vidéo

	var posTimeline = {"x" : 20, "y" : 20, "width" : window.innerWidth-40, "height" : 50}

	var timeline = speechGroup.append("rect")
                         .attr("x", posTimeline.x)
                         .attr("y", posTimeline.y)
                         .attr("width", posTimeline.width)
                         .attr("height", posTimeline.height)
						 .attr("fill", "blue"); 

	

	// Traitement de certaine données
		
	
	/* dataPage_traite
		Les données sur les pages : à partir du nombre de page, et de leurs hauteurs et largeurs, on détermine la hauteur et la largeur sur la page pour les mettre toutes sur la même ligne, et leur position. 
		On va aussi chercher l'image au format jpg
	*/
	
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



	/* dataParagraphe_traite 
		Les données sur les paragraphes : à partir des limites hautes, basses, gauches et droites des paragraphes, on détermine les coordonnées des quatres coins
	*/

	var dataParagraphe_traite = new Array()
		
		for(i = 0; i < dataParagraphe.length; i++)
		{
			var d = dataParagraphe[i];
			var point = new Array()
			
			point[0] = getPoint(dataPage_traite[d.dataset.idpage], d.dataset.left, d.dataset.top)						//en haut à gauche
			point[1] = getPoint(dataPage_traite[d.dataset.idpage], (100 - d.dataset.right), d.dataset.top)				//en haut à droite
			point[2] = getPoint(dataPage_traite[d.dataset.idpage], (100 - d.dataset.right), (100 - d.dataset.bottom))	//en bas à droite
			point[3] = getPoint(dataPage_traite[d.dataset.idpage], d.dataset.left, (100 - d.dataset.bottom))			//en bas à gauche

			dataParagraphe_traite[i] = {'id' : d.id, "page" : d.dataset.idPage, "point" : point, "number" : d.dataset.id}
		}


	
	//Affichage des pages

    var imgs = imageGroup.selectAll("image")
        .data(dataPage_traite)
		.enter()
			.append("svg:image")
			.attr('x',function(d){return d.x;})
			.attr('y',function(d){return d.y;})
			.attr('width', function(d){return d.width;})
			.attr('height', function(d){return d.height;})
			.attr("xlink:href",function(d){return d.src;});


	//Affichage des speechs, paragraphes et liens

	var speech = createSpeech(speechGroup);
	var paragraphe = createParagraphe(paragrapheGroup);
	var link = createLink(linkGroup);


	//Initialisation du mode de visualisation

	var opacity;
	
	modeLine();


	//Sélection des liens à afficher selon les seuils choisis

	selectLink(document.getElementById('nbLink').value, document.getElementById('seuil').value);


/*Affiche les speechs sur la timeline

On leur ajoute deux actions :
	-au passage de la souris, on met en valeur le speech en question, et les liens et les paragraphes qui lui sont liés
	-au clic, on sélectionne le speech et les liens et paragraphes correspondant, et on affiche les informations qui s'y rapportent
*/
function createSpeech(group)
{
	var speech = group.selectAll(".speech")
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


/*Encadre les paragraphes sur les images des pages

On leur ajoute une action :
	-au passage de la souris, on met en valeur le paragraphe en question, et les liens et les speechs qui lui sont liés
*/
function createParagraphe(group)
{
	var paragraphe = group.selectAll(".paragraphe")
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
								.attr("fill", "#fff")
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


/*Prépare sur les liens entre les speechs et les paragraphes, en traçant des lignes

Les liens sont initialisés avec un display none, et ne sont donc pas visible.
Ils seront affichés à deux conditions : (voir la fonction selectLink)
	-On est en mode Line et pas Opacity
	-Les liens appartiennent au seuil décidé

On leur ajoute une action :
	-au passage de la souris (si affiché), on met en valeur le lien en question, et le speech et le paragraphe qu'il relie
*/
function createLink(group)
{
	var link = group.selectAll(".link")
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




