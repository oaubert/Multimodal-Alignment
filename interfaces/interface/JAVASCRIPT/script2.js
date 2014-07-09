var glob_max = 300;

var clickedit;
var lectureEdit;
var memCurrentTime;

function init(value_max)
{
	glob_max = (value_max * $( window ).width()*0.90 / 100);
	lectureEdit = false;
	memCurrentTime = 0;
	glob_BoutonLecture.addEventListener("click", clickEdit, false);

	$(function() {
		$( "#slider-range" ).slider(
		{
			range: true,
			min: 0,
			max: glob_max,
			values: [ 0, glob_max ],
			slide: function( event, ui ) 
			{
				$( "#amount" ).val( getDuree(ui.values[ 0 ]) + " - " + getDuree(ui.values[ 1 ]));
				glob_Pop.currentTime(ui.value * glob_Pop.duration() / glob_max);
			}
		});
		
		$( "#amount" ).val("00:00 - 00:00");
		});


	
}

function getSeconde(value)
{
	var duree = value * glob_Pop.duration() / glob_max;

	return Math.floor(duree);
}


function getDuree(value)
{
	var duree = value * glob_Pop.duration() / glob_max;

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

function clickEdit()
{
	if(!lectureEdit)
	{
		lectureEdit = true;
		memCurrentTime = glob_Pop.currentTime();
		glob_Pop.currentTime($( "#slider-range" ).slider( "values", 0) * glob_Pop.duration() / glob_max);
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

init();
