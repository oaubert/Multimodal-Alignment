var svg = d3.select("#visualisation")
		    .append("svg")
		    .attr("width", window.innerWidth)
		    .attr("height", 200)
		    .style("border", "1px solid black")


	var dataPage_traite = new Array()

		var largeurPage = svg.attr("width") / 2
		
		var d = dataPage[num_page];

		dataPage_traite[0] = {'id' : d.id, "src" : d.src, "x" : 10, "y" : 10, "width" : largeurPage, "height" : d.height * (largeurPage / d.width)}

		if(svg.attr("height") < dataPage_traite[0].y + dataPage_traite[0].height)
		{
			svg.attr("height", dataPage_traite[0].y + dataPage_traite[0].height)
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
			var point = new Array();
			
			for(j = 0; j < 4; j++)
			{
				point[j] = getPoint(dataPage_traite[0], d.data[j].x, d.data[j].y)
			}

			dataParagraphe_traite[i] = {'id' : d.id, "page" : d.page, "data" : point}
		}
	

	var paragraphe = createParagraphe();
	





function createParagraphe()
{
	var paragraphe = svg.selectAll(".paragraphe")
							.data(dataParagraphe_traite)
							.enter()
								.append("polygon")
								.attr("class", "paragraphe")
								.attr("id", function(d){return "paragraphe_" + d.id;})
								.attr("number", function(d){return d.id;})
								.attr("points", function(d)
													{
														var res = "";
														for(i = 0; i < 4; i++)
														{
															res = [res, [d.data[i].x, d.data[i].y].join(",")].join(" ");
														}
														
														return res; 
													})
								.attr("stroke-width", 1)
								.attr("stroke", "green")
								.attr("fill", "transparent")
								.attr("fill-opacity", 0.5);

	return paragraphe;
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



/*Draw the line
var line = svg.append("line")
                         .attr("x1", 5)
                         .attr("y1", 5)
                         .attr("x2", 50)
                         .attr("y2", 50)
                         .attr("stroke-width", 2)
                         .attr("stroke", "black");

var line = svg.append("line")
                         .attr("x1", 500)
                         .attr("y1", 5)
                         .attr("x2", 500)
                         .attr("y2", 200)
                         .attr("stroke-width", 1)
                         .attr("stroke", "green");

var line = svg.append("line")
                         .attr("x1", 100)
                         .attr("y1", 5)
                         .attr("x2", 100)
                         .attr("y2", 200)
                         .attr("stroke-width", 1)
                         .attr("stroke", "green");

var curve = svg.append("path")
				.attr("d", "M 50 50   C 500 100 100 150 200 200")
				.attr("stroke", "blue")
				.attr("stroke-width", 5)
				.attr("fill", "none");

*/
