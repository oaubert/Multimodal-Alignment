/*** Fonction permettant d'afficher et de contrôler la vidéo ***/

/** Permet de passer seulement un passage donné de la vidéo **/

var glob_deb; //Variable globale conservant le début du passage
var glob_fin; //Variable globale conservant la fin du passage


/* Initialise la vidéo
	-Initialise les variables globales
	-Place le temps courant de la vidéo au temps de début
	-Met un listener sur l'update de temps pour vérifier à chaque défilement de la vidéo si le passage est fini : appelle la fonction fini
	-Initialise le bouton play. La vidéo est actuellement en pause
*/
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

/* Vérifie si le passage est fini
	-Test si le temps courant est le temps de fin du passage
	-Si c'est le cas, met la vidéo en pause et désactive le bouton play (le bouton replay est toujours disponible)
*/
function fini()
{
	if(this.currentTime >= glob_fin)
	{
		video.pause();
		buttonPlay.onclick = '';
	}
}

/* Passe de pause à play ou inversement */
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

/* Relance le passage de la vidéo au début */
function replay()
{
	video.currentTime = glob_deb;
	video.play();
	buttonPlay.onclick = playPause;
}
