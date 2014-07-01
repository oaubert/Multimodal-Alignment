var mot1 = "#" + document.getElementById("mot1").value;
var mot2 = "#" + document.getElementById("mot2").value;
var mat_cout = document.getElementById("matrice_cout");
var mat_score = document.getElementById("matrice_score");
var button = document.getElementById("la");
var buttonInit = document.getElementById("init");
var buttonMeilleur = document.getElementById("meilleur");
var res = document.getElementById("res");

var letter1=[];
var letter2=[];
var score = [];

var delta = -10;
var delta_same = 1;
var seuil = 4;

function update()
{
	mot1 = "#" + document.getElementById("mot1").value;
	mot2 = "#" + document.getElementById("mot2").value;

	updateLetter();
	creerMatriceCout();
	button.style="display:block";
}

function go()
{
	initScore();
	valueScore(mot1.length-1, mot2.length-1);
	creerMatriceScore();
	buttonInit.style="display:block";
	buttonMeilleur.style="display:block";
}

function updateLetter()
{
	letter1 = []

	for(i = 0; i < mot1.length; i++)
	{
		c = mot1.charAt(i);
		if(letter1.indexOf(c) == -1)
		{
			letter1.push(c);
		}
	}

	letter2 = []

	for(i = 0; i < mot2.length; i++)
	{
		c = mot2.charAt(i);
		if(letter2.indexOf(c) == -1)
		{
			letter2.push(c);
		}
	}
}

function creerMatriceCout()
{	
	var str = "<tr><td></td>";

	for(i = 0; i < letter1.length; i++)
	{
		str += "<td>" + letter1[i] + "</td>";
	}

	str += "</tr>";

	str += "<tr>";

	for(i = 0; i < letter2.length; i++)
	{
		str += "<tr><td>" + letter2[i] +"</td>";

		for(j = 0; j < letter1.length; j++)
		{
			if(letter1[j] == "#" || letter2[i] == "#")
				str += "<td><input id=\"" + letter1[j] + "_" + letter2[i] + "\" type='text' value='" + delta + "' /></td>";
			else if(String.toLowerCase(letter1[j]) == letter2[i])
				str += "<td><input id=\"" + letter1[j] + "_" + letter2[i] + "\" type='text' value='4' /></td>";
			else
				str += "<td><input id=\"" + letter1[j] + "_" + letter2[i] + "\" type='text' value='-10' /></td>";
		}

		str += "</tr>";
	}

	mat_cout.innerHTML = str;

}

function cout(a,b)
{
	return parseInt(document.getElementById(mot1.charAt(a) + "_" + mot2.charAt(b)).value);
}

function initScore()
{
	score = [];

	for(i = 0; i < mot1.length; i++)
	{
		score.push([]);

		for(j = 0; j < mot2.length; j++)
		{
			score[i].push(-1);
		}
	}

	score[0][0] = Math.max(0,cout(0,0))
}


function valueScore(m,n)
{
	if(score[m][n] != -1)
	{
		return score[m][n];
	}
	else
	{
		if(m == 0)
		{
			score[m][n]	= Math.max(0, valueScore(m,n-1) + cout(0, n));
		}
		else if(n == 0)
		{
			score[m][n] = Math.max(0,valueScore(m-1,n) + cout(m, 0));
		}
		else
		{
			var cout_delta_m = delta;
			var cout_delta_n = delta;

			if(cout(m-1,n) > 0 && mot1.charAt(m-1) == mot1.charAt(m))
				cout_delta_m = delta_same;
			
			if(cout(m,n-1) > 0 && mot2.charAt(n-1) == mot2.charAt(n))
				cout_delta_n = delta_same;

			//alert(cout_delta_n);

			score[m][n] = Math.max(0, valueScore(m-1,n) + cout_delta_m, valueScore(m,n-1) + cout_delta_n, valueScore(m-1,n-1) + cout(m,n))
		}

		return score[m][n];
	}
}


function creerMatriceScore()
{
	var str = "<tr><td></td>";

	for(i = 0; i < mot1.length; i++)
	{
		str += "<td>" + mot1.charAt(i) + "</td>";
	}

	str += "</tr>";

	for(i = 0; i < mot2.length; i++)
	{
		str += "<tr><td>" + mot2.charAt(i) +"</td>";
		
		for(j = 0; j < mot1.length; j++)
		{
			str += "<td class=\"score\" id=\"score_" + j + "_" + i + "\" onclick=\"findAlignement(" + j + ", " + i + ");\">" + score[j][i] + "</td>";
		}

		str += "</tr>";
	}

	mat_score.innerHTML = str;
}

function initAlignement()
{
	all = document.getElementsByClassName("score");

	for(i = 0; i < all.length; i++)
	{
		all[i].style = "background-color:white";
	}
}

function findAlignement(m,n, alignement)
{
	if(!alignement)
	{
		alignement = new Alignement(score[m][n]);
	}


	if(m == 0 && n == 0)
	{
		alignement.stop = [m,n];
		document.getElementById("score_" + m + "_" + n).style = "background-color:green";
	}
	else if(m == 0 && score[m][n] == valueScore(m,n-1) + cout(0, n))
	{
		alignement.alignement.push([m,n]);
		findAlignement(0, n-1, alignement);
		document.getElementById("score_" + m + "_" + n).style = "background-color:red";
	}
	else if(n == 0 && score[m][n] == valueScore(m-1,n) + cout(m, 0))
	{
		alignement.alignement.push([m,n]);
		findAlignement(m-1, 0, alignement);
		document.getElementById("score_" + m + "_" + n).style = "background-color:red";
	}
	else if(m == 0 || n == 0)
	{
		alignement.stop = [m,n];
		document.getElementById("score_" + m + "_" + n).style = "background-color:green";
	}
	else if(m != 0 && n != 0)
	{
		var cout_delta_m = delta;
		var cout_delta_n = delta;

		if(cout(m-1,n) > 0 && mot1.charAt(m-1) == mot1.charAt(m))
			cout_delta_m = delta_same;

		if(cout(m,n-1) > 0 && mot2.charAt(n-1) == mot2.charAt(n))
			cout_delta_n = delta_same;

		if(score[m][n] == valueScore(m-1,n) + cout_delta_m)
		{
			alignement.alignement.push([m,n]);
			findAlignement(m-1, n, alignement);
			document.getElementById("score_" + m + "_" + n).style = "background-color:red";
		}
		else if(score[m][n] == valueScore(m,n-1) + cout_delta_n)
		{
			alignement.alignement.push([m,n]);
			findAlignement(m, n-1, alignement);
			document.getElementById("score_" + m + "_" + n).style = "background-color:red";
		}
		else if(score[m][n] == valueScore(m-1,n-1) + cout(m,n))
		{
			alignement.alignement.push([m,n]);
			findAlignement(m-1, n-1, alignement);
			document.getElementById("score_" + m + "_" + n).style = "background-color:red";
		}
		else if(score[m][n] == "0")
		{
			alignement.stop = [m,n];
			document.getElementById("score_" + m + "_" + n).style = "background-color:green";
		}
		else
		{
			alert("Erreur : " + m + ", " + n);
		}
	}

	return alignement;
}

function meilleursAlignement()
{
	var aligns = [];
	var use = [];

	for(i = 0; i < score.length; i++)
	{
		use[i] = []
		for(j = 0; j < score[i].length; j++)
		{
			use[i][j] = []
		}
	}

	for(i = score.length-1; i >= 0; i--)
	{
		for(j = score[i].length-1; j >= 0; j--)
		{
			
			if(score[i][j] > seuil)
			{
				if(use[i][j].length > 0)
				{
					for(k = 0; k < use[i][j].length; k++)
					{
						if(score[i][j] > aligns[use[i][j][k]].score)
						{
							aligns.splice(use[i][j][k], 1, findAlignement(i,j));
						}
					}
				}
				else
				{
					align = findAlignement(i,j);
					aligns.push(align);

					for(k = 0; k < align.alignement.length; k++)
					{	
						use[align.alignement[k][0]][align.alignement[k][1]].push(aligns.length-1);

						//document.getElementById("score_" + align.alignement[k][0] + "_" + align.alignement[k][1]).innerHTML += "*";
					}
				}
				
			}
		}
	}

	initAlignement();

	for(i = 0; i < aligns.length; i++)
	{
		document.getElementById("score_" + aligns[i].alignement[0][0] + "_" + aligns[i].alignement[0][1]).style = "background-color:red";
	}

	/*long = aligns[0];

	for(i = 1; i < aligns.length; i++)
	{
		if(long.alignement.length < aligns[i].alignement.length)
		{
			long = aligns[i];
		}
	}

	colorAlignement(long);
*/	
}

function colorAlignement(alignement)
{
	for(i = 0; i < alignement.alignement.length; i++)
	{
		document.getElementById("score_" + alignement.alignement[i][0] + "_" + alignement.alignement[i][1]).style = "background-color:red";
	}

	document.getElementById("score_" + alignement.stop[0] + "_" + alignement.stop[1]).style = "background-color:green";
}
	


/** Classe Alignement **/


function Alignement(score)
{
	this.score = score;
	this.alignement = [];
	this.stop;
	this.estDans = estDans;
}

function estDans(m,n,debut,fin)
{
	//alert(debut + "_" + fin);
	milieu = Math.floor((fin+debut)/2);
	score_milieu = this.alignement[milieu];

	if(fin > debut)
		return false;

	if(m < score_milieu[0])
	{
		return this.estDans(m,n, debut, milieu-1)
	}
	else if(m > score_milieu[0])
	{
		return this.estDans(m,n, milieu+1, fin)
	}
	else //m == score_milieu[0]
	{
		if(n < score_milieu[1])
		{
			return this.estDans(m,n, debut, milieu-1)
		}
		else if(n > score_milieu[1])
		{
			return this.estDans(m,n, milieu+1, fin)
		}
		else //n == score_milieu[1]
		{
			return true;
		}
	}
}
