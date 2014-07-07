var glob_deb;
var glob_fin;

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
