function chargerDocument()
{
	var id = 0;
	var style;
	var string = "";
	var paragraphe;

	for(i = 0; i < dataPage.length; i++)
	{
		paragraphe = $(".data_paragraphe[data-idPage=\"" + dataPage[i].dataset.id + "\"]");
		string += "<div id=\"pdf_affiche\" style=\"position:relative;\" width='100%' height='100%' display='inline'>"
		
		for(j = 0; j < paragraphe.length; j++)
		{
			string += "<a id='" + id + "' onClick='SynchroniseVideo(" + id + ")' time='" + "0.0_0.0" + "' "; //time pourra être remplacé par les temps de dataLink -- lequel ?
			style = "top:" + paragraphe[j].dataset.top + "%; left:" + paragraphe[j].dataset.left + "%; right:" + paragraphe[j].dataset.right + "%; bottom:" + paragraphe[j].dataset.bottom + "%;";
            string += "style='position:absolute; " + style + " z-index:1;' ";
            string += "title='" + "0.0_0.0" + "' "; //title pourra être remplacé par les temps de dataLink
            string += "onmouseout=\"this.style.background='rgba(0, 0, 0, 0)';\" onmouseover=\"this.style.background='rgba(4, 133, 157, 0.15)';\">";
            string += "</a>";

			id = id + 1;
		}

		string += "<img src='" + chemin + "img/PICTURE_" + dataPage[i].dataset.numero + ".jpg' style='position:relative; top:0px; left:0px;' width='100%'/></div>";
	}			

	$("#tdTexte").html(string);
}
