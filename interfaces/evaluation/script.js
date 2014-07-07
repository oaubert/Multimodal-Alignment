var glob_deb;
var glob_fin;
var dataSpeech;
var dataLink;
var res = {};
var idSpeech = 0;

function initialisation(debut, fin)
{
	glob_deb = debut;
	glob_fin = fin;

	video = document.getElementById("video");
	video.currentTime = glob_deb;
	video.addEventListener('loadedmetadata', function() {this.currentTime = glob_deb;}, false); //Au cas où
	video.addEventListener('timeupdate', fini, false);
	buttonPlay = document.getElementById("play");
}

function fini()
{
	if(this.currentTime >= glob_fin)
	{
		video.pause();
		buttonPlay.onclick = '';
	}
}

function playPause()
{
	if(video.paused)
	{
		video.play();
		buttonPlay.innerHTML = "Pause";
	}
	else
	{
		video.pause();
		buttonPlay.innerHTML = "Play";
	}
}
	
function replay()
{
	video.currentTime = glob_deb;
	video.play();
	buttonPlay.onclick = playPause;
}

function afficherParagraphe(n, baliseSimilarite, baliseTexte)
{
	var link = dataLink[n];
	document.getElementById(baliseSimilarite).innerHTML = link.dataset.similarite;

	var paragraphe = $(".data_paragraphe[data-id=\"" + link.dataset.idparagraphe + "\"]");

	document.getElementById(baliseTexte).innerHTML = paragraphe.html();	
}


function afficher()
{
	if(idSpeech >= nbSpeech)
	{
		location.href="fini.php";
	}

	$("input[type='radio']").prop("checked", false);

	dataSpeech = d3.selectAll(".data_speech[data-id=\"" + idSpeech + "\"]")[0];
	dataLink = d3.selectAll(".data_link[data-idspeech=\"" + idSpeech + "\"]")[0];

	var debut = dataSpeech[0].dataset.begin;
	var fin = dataSpeech[0].dataset.end;

	afficherParagraphe(0, "similarite1", "texte1");
	afficherParagraphe(1, "similarite2", "texte2");
	afficherParagraphe(2, "similarite3", "texte3");

	initialisation(debut, fin);
}


function resultat()
{
	res[idSpeech] = {"1" : document.getElementById('p1_Oui').checked, "2" : document.getElementById('p2_Oui').checked, "3" : document.getElementById('p3_Oui').checked};

	idSpeech = idSpeech + 1;

	afficher();
}

function resetEvaluation()
{
	res = {};

	idSpeech = 0;

	afficher();
}
