var glob_TableauIntervals = []; //glob_TableauIntervals est un tableau d'Interval, il contient les intervals de temps pour chaque paragraphe
var glob_TableauIdsActifs = []; //Tableau qui recense tous les id mis en �vidences � l'instant t

var glob_ParagrapheCourant = 0; //Le paragraphe mis en valeur � l'instant t
var glob_Video = null; //Notre video html5
var glob_Pop = null; //L'instanciation de la vid�o dans pop
var glob_Mute = false; //Le son est il activ�? true: non, false: oui
var glob_Lecture = false; //La vid�o est elle en lecture? true: oui, false: non
var glob_AncienVolume = null; //Le volume avant que le son n'ai �t� coup�
var glob_BoutonSynchronisation = null; //Le bouton permettant d'activer ou de supprimer la synchronisation
var glob_BoutonLecture = null; //Le bouton permettant de mettre en lecture ou en pause
var glob_BoutonMute = null; //Le bouton permettant de muter ou de remettre le son
var glob_BarreVolume = null; //La barre permettant de regler le volume
var glob_BarreTemps = null; //La barre permettant de se placer � l'instant t de la vid�o
var glob_ProgressBarTemps = null; //glob_BarreTemps instanci� dans progressBar.js
var glob_AfficheurTemps = null; //L'afficheur de type hh:mm:ss, qui permet d'afficher l'instant t

var glob_tailleProgressBar = 300;

var onLectureEdit = false;

/*
 * Lanc�e au chargement de la page
 * Elle permet d'initialiser tous les composants de la page
 */
function initialisation(v, tailleProgressBar, edit) {
    //Initialisation de la vid�o et instanciation dans popcorn
    glob_Video = v;
    glob_Pop = Popcorn(glob_Video);
    //Generation dtu tableau contenu dans glob_TableauIntervals
    genererTableauInterval();
    //Recuperation des diff�rents �l�ments du player afin de les stocker dans des variables
    glob_BoutonSynchronisation = document.getElementById('btn_active');
    glob_BoutonLecture = document.getElementById("btn_play");
    glob_BoutonMute = document.getElementById("btn_mute");
    glob_AfficheurTemps = document.getElementById("time");
    glob_BarreTemps = document.getElementById("timeline");
	glob_tailleProgressBar = (tailleProgressBar * $( window ).width()*0.90 / 100);

    //Ajout des �couteurs sur les diff�rents boutons 
	if(!edit)
    	glob_BoutonLecture.addEventListener("click", Lecture, false);
	else
		glob_BoutonLecture.addEventListener("click", LectureEdit, false);

    glob_BoutonMute.addEventListener("click", Mute, false);
    ChargementCtrlTemps();
    //Ajout des �couteurs pour la vid�o
    glob_BarreTemps.addEventListener("mousedown", MiseAJourTemps, false);
    glob_Video.addEventListener("timeupdate", MiseAJourTempsBis, false);
    //Mise en lecture de la vid�o, et chargement du la barre de volume et de temps
    Lecture();
    ChargementCtrlVolume(); 


	//Pour l'�dition
	if(edit)
	{
		onLectureEdit = false;

		glob_Video.addEventListener("timeupdate", MiseAJourTempsBisEdit, false);

		$(function() {
			$( "#slider-range" ).slider(
			{
				range: true,
				min: 0,
				max: glob_tailleProgressBar,
				values: [ 0, glob_tailleProgressBar ],
				slide: function( event, ui ) 
				{
					onLectureEdit = false;
					$( "#amount" ).val( getDuree(ui.values[ 0 ]) + " - " + getDuree(ui.values[ 1 ]));
					Pause();
					glob_Pop.currentTime(ui.value * glob_Pop.duration() / glob_tailleProgressBar);
				}
			});
		
			$( "#amount" ).val("00:00 - 00:00");
			});   
	}
}

/*
 * Fonction qui genere les deux tableau utiles � ce logiciel
 */
function genererTableauInterval(){
    var previousBegin = 0, previousEnd = 0;
    for(var i = 0; i < taille(); i++){
        var tab = document.getElementById(i).getAttribute('time').split("_"),
            debut = tab[0],
            fin = tab[1];
        if (+debut === 0 && +fin === 0) {
            debut = previousBegin;
            fin = previousEnd;
        }
        glob_TableauIntervals[i] = new Interval(debut, fin);
        glob_TableauIdsActifs[i] = false; //aucune mis en evidence des paragraphes
        previousBegin = debut;
        previousEnd = fin;
    }
}

/*
 * Classe permettant d'instancier des intervals de temps
 */
function Interval(debut, fin) { 
    this.debut = debut;
    this.fin = fin;
}
/*
 * Fonction qui retourne le nombre d'�l�ments � traiter par la fonction genererTableauInterval()
 */     
function taille(){
        var i = 0;
        while(document.getElementById(i)){
                i++;
        }
        return i;
}

/*
 * Fonction qui met en lecture ou en pause en fonction de la variable glob_Lecture
 */
function Lecture() {
	if(glob_Lecture){
	    glob_BoutonLecture.innerHTML = "<img src=\"../../IMAGE_boutons/play.png\" />";
	    glob_Pop.pause();
	    glob_Lecture = false;
	}
	else{
	    glob_BoutonLecture.innerHTML = "<img src=\"../../IMAGE_boutons/pause.png\" />";
	    glob_Pop.play();
	    glob_Lecture = true;
	}
}

function Pause()
{	
	glob_BoutonLecture.innerHTML = "<img src=\"../../IMAGE_boutons/play.png\" />";
    glob_Pop.pause();
    glob_Lecture = false;
}

function Play()
{
	glob_BoutonLecture.innerHTML = "<img src=\"../../IMAGE_boutons/pause.png\" />";
    glob_Pop.play();
    glob_Lecture = true;
}

/*
 * Fonction qui d�sactive le son ou l'active, en fonction de la variable glob_Mute
 */
function Mute() {
    if(glob_Mute){
        glob_Pop.unmute();
        glob_Pop.volume(glob_AncienVolume);
        glob_BarreVolume.value = glob_AncienVolume;
        glob_BoutonMute.innerHTML = "<img src=\"../../IMAGE_boutons/volume.png\" />";
        glob_Mute = false;
    }
    else{
        glob_AncienVolume = glob_Pop.volume();
        glob_BarreVolume.value = 0;
        glob_BoutonMute.innerHTML = "<img src=\"../../IMAGE_boutons/mute.png\" />";
        glob_Pop.mute();
        glob_Mute = true;
    }
    
}

/*
 * Fonction qui initialise le contr�le du temps
 */
function ChargementCtrlTemps(){	
	var i = 500;
    glob_ProgressBarTemps = new ProgressBar("timeline",{
		width: glob_tailleProgressBar,
		height: 32,
		minValue: 0,
		maxValue: glob_tailleProgressBar,
		showLabel: false,
		orientation: ProgressBar.Orientation.Horizontal,
		direction: ProgressBar.Direction.LeftToRight,
		imageUrl: '../../IMAGE_boutons/foretimeline.png',
		backgroundUrl: '../../IMAGE_boutons/backtimeline.png'
	})
;}

/*
 * Fonction qui s'effectue � chaque modification du temps
 */
function MiseAJourTemps(e){
    Lecture();
    var posX = e.clientX;
    var el = glob_BarreTemps;
    if(el.offsetParent){
        var marge = el.offsetLeft;
        while(el = el.offsetParent) {    
            marge += el.offsetLeft;
        }
    }
    glob_ProgressBarTemps.setValue(posX - marge);
    glob_Pop.currentTime((posX-marge)*glob_Pop.duration()/glob_tailleProgressBar);
    document.onmousemove = ModificationBarreTemps;
    document.onmouseup = StopModificationBarreTemps;
}

/*
 * Fonction qui s'active durant un cliquer-glisser sur la barre de temps. Modifie son apparence et la vid�o
 */
function ModificationBarreTemps(e){
    var posX = e.clientX;
    var el = glob_BarreTemps;
    if(el.offsetParent){
        var marge = el.offsetLeft;
        while(el = el.offsetParent) {    
            marge += el.offsetLeft;
        }
    }
    glob_ProgressBarTemps.setValue(posX - marge);
    glob_Pop.currentTime((posX-marge)*glob_Pop.duration()/glob_tailleProgressBar);
    document.body.focus();
    //Empecher la selection de texte
    document.onselectstart = function() {
       return false;
    };
    glob_Video.ondragstart = function() {
       return false;
    };
    return false;
}

/*
 * Fonction qui s'active lorsque l'utilsateur arr�te de cliquer sur la barre de temps. Arrete la modification de celle ci
 */
function StopModificationBarreTemps(e){
    document.onmouseup = null;
    document.onmousemove = null;
    Lecture();
}

/*
 * Fonction qui s'active � chaque instant, met � jour l'afficheur de temps et la barre
 */
function MiseAJourTempsBis(){
    MiseAJourAfficheur();
    MiseEnEvidenceParagraphe();
    ModifierProgressBarre();
}

/*
 * Fonction qui met � jour l'afficheur de temps
 */
function MiseAJourAfficheur(){
    var sec= glob_Pop.currentTime();
    var duree = glob_Pop.duration();
    var h = Math.floor(sec/3600);
    vec=sec%3600;
    var min =Math.floor(sec/60);
    sec = Math.floor(sec%60);
    if (sec.toString().length < 2) sec="0"+sec;
    if (min.toString().length < 2) min="0"+min;
    var ht = Math.floor(duree/3600);
    duree=duree%3600;
    var mint =Math.floor(duree/60);
    duree = Math.floor(duree%60);
    if (duree.toString().length < 2) duree="0"+duree;
    if (mint.toString().length < 2) mint="0"+mint;
    time.innerHTML = h+":"+min+":"+sec+"/"+ht+":"+mint+":"+duree;
}

/*
 * Fonction qui met en �vidence le paragraphe correspondant au temps courant
 */
function MiseEnEvidenceParagraphe() {
    var duree = glob_Pop.duration();
    var current = glob_Pop.currentTime();
    if (current > duree) {
        clearInterval(glob_AfficheurTempsr);
    }
    else {
        for (var i = 0; i < glob_TableauIntervals.length; i++) {
            if (current >= glob_TableauIntervals[i].debut && current < glob_TableauIntervals[i].fin) {
                if (!glob_TableauIdsActifs[i]) AjouterMiseEnEvidence(i);
            }
            else {
                if (glob_TableauIdsActifs[i]) SupprimerMiseEnEvidence(i);
            }
        }
    }
}

/*
 * Fonction qui modifie l'apparence de glob_ProgressBarTemps
 */
function ModifierProgressBarre(){
    glob_ProgressBarTemps.setValue(glob_Pop.currentTime()*glob_tailleProgressBar/glob_Pop.duration());
}

/*
 * Fonction qui initialise le contr�le du volume
 */
function ChargementCtrlVolume() {
    glob_BarreVolume = document.getElementById("volume");
    glob_BarreVolume.value = glob_Pop.volume();
    glob_BarreVolume.addEventListener("change", function(e) {
        myVol = e.target.value;
        if (myVol == 0) {
            glob_Mute = true;
            glob_Pop.mute();
            glob_BoutonMute.innerHTML = "<img src=\"../../IMAGE_boutons/mute.png\" />";
        } else {
            glob_Pop.unmute();
            glob_Pop.volume(myVol);
            glob_Mute = false;
            glob_BoutonMute.innerHTML = "<img src=\"../../IMAGE_boutons/volume.png\" />";
        }
        return false;
    }, true);
}

/*
 * Fonction qui modifie le temps courant pour le synchronis� avec l'�l�ment paragraphe cliqu�
 */
function SynchroniseVideo(id) {
    glob_Pop.currentTime(glob_TableauIntervals[id].debut);
}

/*
 * Ajoute un �l�ment au tableau des paragraphes mis en �vidence
 */
function AjouterMiseEnEvidence(id) {
    document.getElementById(id).style.border = "solid 1px #04859D";
    glob_TableauIdsActifs[id]=true;
    if (glob_BoutonSynchronisation.checked==true) {
        window.location.hash = "#" + id;}
}

/*
 * Supprime un �l�ment du tableau des paragraphe mis en �vidence
 */
function SupprimerMiseEnEvidence(id) {
    document.getElementById(id).style.border = "solid 0px";
    glob_TableauIdsActifs[id]=false;
}

/*
 * Fonction qui permet � l'utilisateur de modifier l'interval du paragraphe id
 */
function ModificationSynchronisation(id) {
	begin = getSeconde($( "#slider-range" ).slider("values", 0));
	end = getSeconde($( "#slider-range" ).slider("values", 1));
	location.href="modification_xml.php?id="+id+"&begin="+begin+"&end="+end;
}

var posXstart; // La position X de d�part de la souris
var posYstart; // La position Y de d�part de la souris
var taille; // La taille initiale de la glob_Video
var tailleTexte; //La taille initiale du PDF
var taille2;

/*
 * Fonction qui se d�clenche au clic sur la vid�o
 * Elle permet de modifier la taille de la vid�o et du pdf d'un simple cliquer glisser
 */
function DebutModificationTailleVideo(e){
   posXstart = e.clientX;
   posYstart = e.clientY;
   taille = document.getElementById('video').offsetWidth;
   tailleTexte = document.getElementById('tdTexte').offsetWidth;
   document.onmousemove = ModifierTailleVideo;
   document.onmouseup = StopModifierTailleVideo;
   document.body.focus();
   //On d�sactive la s�lection de texte
   document.onselectstart = function() {
       return false;
   };
   glob_Video.ondragstart = function() {
       return false;
   };
   return false;
}

/*
 * Fonction qui se d�clenche tant que le clic reste appuy�
 */
function ModifierTailleVideo(e){
    var posXnew = e.clientX;
    var newTaille = taille + posXnew - posXstart;
    hauteur = document.getElementById('video').offsetHeight;
    taillediv = document.getElementById('milieu').offsetWidth;
    rapport = document.getElementById('video').offsetWidth/hauteur;
    if(hauteur < 594 || newTaille < taille2){
	if(hauteur > 100 || newTaille > taille2){
            document.getElementById('video').style.width = newTaille+"px";
            document.getElementById('texte').style.width = taillediv-newTaille-11+"px";
            taille2 = document.getElementById('video').offsetWidth;
            newhauteur = document.getElementById('video').offsetHeight;
            if(newhauteur > 594){
                ajust = 594*rapport;
                document.getElementById('video').style.width = ajust+"px";
                document.getElementById('texte').style.width = taillediv-ajust-11+"px";
            }
        }
    }
}

/*
 * Fonction qui se d�clenche d�s que le clic est relach�
 */
function StopModifierTailleVideo(e){
   document.onmousemove = null;
   document.onmouseup = null;
   document.body.focus();
   //On r�active la s�lection de texte
   document.onselectstart = null;
   glob_Video.ondragstart = null;
   return true;
}





// Fonctions d'�dition


function LectureEdit()
{
	if(!onLectureEdit)
	{
		onLectureEdit = true;
		glob_Pop.currentTime($( "#slider-range" ).slider( "values", 0) * glob_Pop.duration() / glob_tailleProgressBar);
		Play();
	}
	else
		Lecture();
}

function stopLectureEdit()
{
	if(onLectureEdit)
	{
		Pause();
		onLectureEdit = false;
	}
}


function getSeconde(value)
{
	var duree = value * glob_Pop.duration() / glob_tailleProgressBar;

	return Math.floor(duree);
}


function getDuree(value)
{
	var duree = value * glob_Pop.duration() / glob_tailleProgressBar;

    var curmins = Math.floor(duree / 60);
    var cursecs = Math.floor(duree - curmins * 60);

    if (cursecs < 10) {
        cursecs = "0" + cursecs;
    }

    if (curmins < 10) {
        curmins = "0" + curmins;
    }

    return curmins + ":" + cursecs;
}


function MiseAJourTempsBisEdit(){
	if(glob_ProgressBarTemps.value >= $( "#slider-range" ).slider("values", 1))
	{
		stopLectureEdit();
	}
}

