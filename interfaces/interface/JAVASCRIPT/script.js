var clickedit;
var champsStart;
var champsEnd;
var lectureEdit;
var suiviLectureEdit;
var memCurrentTime;

function init()
{
	lectureEdit = false;
	memCurrentTime = 0;
	champsStart = document.getElementById("sliderStart");
	champsEnd = document.getElementById("sliderEnd");
	clickedit = document.getElementById("playEdit");
	clickedit.addEventListener("click", clickEdit, false);
}

function inputStart(input)
{
	start = parseInt(input.value)
	end = parseInt(document.getElementById('valueEnd').value);
	if(start <= end)
	{
		document.getElementById('valueStart').value = input.value;
		inputUpdate(input, document.getElementById('tempsStart'));
	}
	else
		document.getElementById('sliderStart').value = end;
}

function inputEnd(input)
{
	start = parseInt(document.getElementById('valueStart').value);
	end = parseInt(input.value);
	if(start <= end)
	{	
		document.getElementById('valueEnd').value = input.value;
		inputUpdate(input, document.getElementById('tempsEnd'));
	}
	else
		document.getElementById('sliderEnd').value = start;
}



// updating time, with maths & shit
function inputUpdate(input, value) 
{
	var duree = input.value * glob_Pop.duration() / 300;

    var curmins = Math.floor(duree / 60);
    var cursecs = Math.floor(duree - curmins * 60);

    if (cursecs < 10) {
        cursecs = "0" + cursecs;
    }

    if (curmins < 10) {
        curmins = "0" + curmins;
    }

    value.innerHTML = curmins + ":" + cursecs;
}


function clickEdit()
{
	if(!lectureEdit)
	{
		Lecture();
		lectureEdit = true;
		memCurrentTime = glob_Pop.currentTime();
		glob_Pop.currentTime(parseInt(champsStart.value) * glob_Pop.duration() / 300);
		glob_Pop.play();
	}
	else
		stopLectureEdit();
}

function stopLectureEdit()
{
	if(lectureEdit)
	{
		glob_Pop.currentTime(memCurrentTime);
		glob_Pop.pause();
	
		lectureEdit = false;
	}
}




/*Liaison du fragment vidéo à un paragraphe*/
