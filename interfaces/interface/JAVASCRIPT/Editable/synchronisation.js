var tableau = [];
var queue = []; //finalement, pas queue //file (en francais) first in, first out (FIFO) //tableau initialisé dans genererTab() et modifié dans updateText(), ajout(), supprimer()

var id_current = 0;
var video = null;
var pop = null;
var muted = false;
var player = false;
var old_vol = null;
var btn_active = null;
var btn_play = null;
var btn_mute = null;
var btn_volume = null;
var timeline = null;
var time = null;
var progress;

function Interval(debut, fin) {
    this.debut = debut;
    this.fin = fin;
}

function initialisation(v) {    

    //Création d'une vidéo popCorn
    video = v;
    pop = Popcorn(video);
    //Lancement de la vidéo et du controle du volume    
    genereTab();
    //Récupération des différents boutons du controleur
	btn_active = document.getElementById('btn_active');
    btn_play = document.getElementById("btn_play");
    btn_mute = document.getElementById("btn_mute");
    time = document.getElementById("time");
    timeline = document.getElementById("timeline");
    
    //Ajout des écouteurs pour le controleur
    btn_play.addEventListener("click", play, false);
    btn_mute.addEventListener("click", mute, false);
    timeline.addEventListener("mousedown", timelineUpdate, false);
    
    loadTimeline();

//Ajout des écouteurs pour la vidéo
    video.addEventListener("timeupdate", OnTimeUpdate, false);
    play();
    ctrl_volume();
}
function timelineUpdate(e){
    pop.pause();
    posX = e.clientX;
    el = timeline;
    if(el.offsetParent){
        marge = el.offsetLeft;
        while(el = el.offsetParent) {    
            marge += el.offsetLeft;
        }
    }
    laTimeline.setValue(posX - marge);
    pop.currentTime((posX-marge)*pop.duration()/300);
    document.onmousemove = modifTimeline;
    document.onmouseup = stopModif;
}

function modifTimeline(e){
    posX = e.clientX;
    el = timeline;
    if(el.offsetParent){
        marge = el.offsetLeft;
        while(el = el.offsetParent) {    
            marge += el.offsetLeft;
        }
    }
    laTimeline.setValue(posX - marge);
    pop.currentTime((posX-marge)*pop.duration()/300);
    document.body.focus();

    // prevent text selection in IE
    document.onselectstart = function() {
       return false;
    };
    // prevent IE from trying to drag an image
    video.ondragstart = function() {
       return false;
    };

    // prevent text selection (except IE)
    return false;

}

function stopModif(e){
    document.onmousedown = null;
    document.onmousemove = null;
    pop.play();
}

function updateprogress(){
    laTimeline.setValue(pop.currentTime()*300/pop.duration());
}

var laTimeline;
function loadTimeline(){
    laTimeline = new ProgressBar("timeline",{
		width: 300,
		height: 32,
		minValue: 0,
		maxValue: 300,
		showLabel: false,
		orientation: ProgressBar.Orientation.Horizontal,
		direction: ProgressBar.Direction.LeftToRight,
		imageUrl: '../../../IMAGE_boutons/foretimeline.png',
		backgroundUrl: '../../../IMAGE_boutons/backtimeline.png'
	})
;}
        
function taille(){
        var i = 0;
        while(document.getElementById(i)){
                i++;
        }
        return i;
}
function genereTab(){
    for(i = 0; i < taille(); i++){
        var tab = document.getElementById(i).getAttribute('time').split("_");	
        var debut = tab[0];
        var fin = tab[1];
        tableau[i] = new Interval(debut, fin);
        queue[i]=false; //aucune mis en evidence des paragraphes
    }
}
//A chaque fois que le temps courant change, on éxécute ces deux fonctions
function OnTimeUpdate(){
    updateTime();
    updateText();
    updateprogress();
}

//Fonction qui modifie l'apparence et la valeur de la timeline
function updateTimeLine(){
    pop.pause();
    var duree = pop.duration();
    var tps = timeline.value;
    pop.currentTime(tps*duree);
    pop.play();
}

//Fonction qui affiche le temps en h/min/s
function updateTime(){
    var sec= pop.currentTime();
    var duree = pop.duration();
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
    timeline.value = pop.currentTime()/pop.duration();
}

//Fonction qui permet le controle du volume
function ctrl_volume() {
    btn_volume = document.getElementById("volume");
    btn_volume.value = pop.volume();
    btn_volume.addEventListener("change", function(e) {
        myVol = e.target.value;
        if (myVol == 0) {
            muted = true;
            pop.mute();
            btn_mute.innerHTML = "<img src=\"../../../IMAGE_boutons/mute.png\" />";
        } else {
            pop.unmute();
            pop.volume(myVol);
            muted = false;
            btn_mute.innerHTML = "<img src=\"../../../IMAGE_boutons/volume.png\" />";
        }
        return false;
    }, true);
}

//Fonction qui mute/demute en fonction de l'état
function mute() {
    if(muted){
        pop.unmute();
        pop.volume(old_vol);
        btn_volume.value = old_vol;
        btn_mute.innerHTML = "<img src=\"../../../IMAGE_boutons/volume.png\" />";
        muted = false;
    }
    else{
        old_vol = pop.volume();
        btn_volume.value = 0;
        btn_mute.innerHTML = "<img src=\"../../../IMAGE_boutons/mute.png\" />";
        pop.mute();
        muted = true;
    }
    
}

//Fonction qui play/pause en fonction de l'état
function play() {
    if(player){
        btn_play.innerHTML = "<img src=\"../../../IMAGE_boutons/play.png\" />";
        pop.pause();
        player = false;
    }
    else{
        btn_play.innerHTML = "<img src=\"../../../IMAGE_boutons/pause.png\" />";
        pop.play();
        player = true;
    }
}



//Fonction qui met en évidence le texte correspondant au temps courant
function updateText() {
    var duree = pop.duration();
    var current = pop.currentTime();
    if (current > duree) {
        clearInterval(timer);
    }
    else {
        //if (current < tableau[id_current].debut || current >= tableau[id_current].fin) {
            for (var i = 0; i < tableau.length; i++) {
                if (current >= tableau[i].debut && current < tableau[i].fin) {
                    if (!queue[i]) ajout(i); //ajout de l'id dans la liste des éléments mis en évidence
                    /*var id1 = id_current.toString();
                    var id2 = i.toString();
                    inverse(id1, id2);
                    id_current = i;*/
                }
                else {
                    if (queue[i]) supprimer(i);
                }
            }
        //}
    }
}

//Fonction qui modifie le temps courant au clic sur un lien
function setPlayer(id) {
    pop.currentTime(tableau[id].debut);
}

//stockage des élément mis en évidence
function ajout(id) {
    document.getElementById(id).style.border = "solid 1px #04859D";
    queue[id]=true;
    if (document.getElementById('btn_active').checked==true) {
        window.location.hash = "#" + id;}
}

//désactivation des éléments
function supprimer(id) {
    document.getElementById(id).style.border = "solid 0px";
    queue[id]=false;
}

//Fonction qui modifie la synchronize
function setSynchro(id) {
	var test = false;
	var modifDebut = window.prompt("Entrez votre nouveau temps de début en seconde", "");
	if ((modifDebut<0)||(modifDebut>=pop.duration())||(isNaN(modifDebut)==true)){
		test = true;
	}
	
	if (test != true) {
		var modifFin = window.prompt("Entrer votre nouveau temps de fin", "");
		if ((modifFin<0)||(modifFin<=modifDebut)||(isNaN(modifFin)==true)||(modifFin>pop.duration())){
			test = true;
		}
	}
	
	if (test == true) {
		alert("durée non valide");
	}
	
	else {
			tableau[id].debut=modifDebut;
			tableau[id].fin=modifFin;
	}
}

//Fonction qui inverse la mise en évidence des deux éléments donnés
function inverse(id1, id2) {
    document.getElementById(id1).style.border = "solid 0px";
    document.getElementById(id2).style.border = "solid 1px #04859D";
	if (document.getElementById('btn_active').checked==true) {
		window.location.hash = "#" + id2;}
}

var posXstart;            // les position de départ de la souris
var posYstart;
var taille;// la taille initiale de la video
var tailleTexte;

function OnMouseDown(e)
{
   posXstart = e.clientX;
   posYstart = e.clientY;
   taille = document.getElementById('video').offsetWidth;
   tailleTexte = document.getElementById('tdTexte').offsetWidth;
   document.onmousemove = OnMouseMove;
   document.onmouseup = OnMouseUp;
   document.body.focus();

   // prevent text selection in IE
   document.onselectstart = function() {
       return false;
   };
   // prevent IE from trying to drag an image
   video.ondragstart = function() {
       return false;
   };

   // prevent text selection (except IE)
   return false;

}

var taille2;
function OnMouseMove(e)
{
   var posXnew = e.clientX;
   var newTaille = taille + posXnew - posXstart;
   var newTexte = tailleTexte - posXnew + posXstart;
   hauteur = document.getElementById('video').offsetHeight;
   if(hauteur < 590 || newTaille < taille2){
		if(hauteur > 100 || newTaille > taille2){
			document.getElementById('video').style.width = newTaille+"px";
			document.getElementById('texte').style.width = newTexte+"px";
			taille2 = document.getElementById('video').offsetWidth;
		}
    }
}

function OnMouseUp(e)
{
   document.onmousemove = null;
   document.onmousedown = null;
   document.body.focus();

   // prevent text selection in IE
   document.onselectstart = null;
   // prevent IE from trying to drag an image
   video.ondragstart = null;

   // prevent text selection (except IE)
   return true;
   }