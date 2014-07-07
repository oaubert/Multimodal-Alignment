<!DOCTYPE html>
<?php 
	$chemin = "../data/" . $_GET['document'] . '/';
?>
<html>
    <head>
        <title>Test Alignement Local</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<link href="style.css" rel="stylesheet" type="text/css">
		<script src="script.js"></script>
		<link rel="stylesheet" type="text/css" href="../../js/jquery/css/ui-lightness/jquery-ui-1.10.4.custom.min.css">
		<script type="text/javascript" src="../../js/d3/d3.min.js"></script>
		<script type="text/javascript" src="../../js/jquery/js/jquery-1.10.2.js"></script>
		<script type="text/javascript" src="../../js/jquery/js/jquery-ui.min.js"></script>
    </head>
	<body onload="afficher();">    

		<div id="data">
			<?php
				include($chemin . "paragraphe.html");
				include($chemin . "speech.html");
				include($chemin . "page.html");
				include($chemin . "alignement.html");
			?>
		</div>

		<script type="text/javascript">
			var nbSpeech = d3.select("#data_transcript")[0][0].dataset.number;
			var chemin = "<?php echo $chemin ?>";
		</script>

		<video class="drag" width="45%" id="video" height="100%" controls="controls">
			<source src="<?php echo $chemin ?>video.webm">
			<code>video</code>
		</video>

		<div id="controls">
			<button type="button" id="play" onclick="playPause()">Play</button>
			<button type="button" id="replay" onclick="replay()">Replay</button>
		</div>

		<div id="paragraphe">
			Paragraphe 1 : &nbsp;&nbsp;&nbsp; <span id="similarite1"></span><div id="texte1"></div>
			Paragraphe 2 : &nbsp;&nbsp;&nbsp; <span id="similarite2"></span><div id="texte2"></div>
			Paragraphe 3 : &nbsp;&nbsp;&nbsp; <span id="similarite3"></span><div id="texte3"></div>
		</div>

		<form action="" method="post">
			<div id="formulaire">
				<div id="div_p1">
					Paragraphe 1 : 
					<label for="p1_Oui">Oui</label><input id="p1_Oui" type="radio" name="p1" value="Oui" required="required"/>
					<label for="p1_Non">Non</label><input id="p1_Non" type="radio" name="p1" value="Non" required="required"/>
				</div>
				<div id="div_p2">
					Paragraphe 2 : 
					<label for="p2_Oui">Oui</label><input id="p2_Oui" type="radio" name="p2" value="Oui" required="required"/>
					<label for="p2_Non">Non</label><input id="p2_Non" type="radio" name="p2" value="Non" required="required"/>
				</div>
				<div id="div_p2">
					Paragraphe 3 : 
					<label for="p3_Oui">Oui</label><input id="p3_Oui" type="radio" name="p3" value="Oui" required="required"/>
					<label for="p3_Non">Non</label><input id="p3_Non" type="radio" name="p3" value="Non" required="required"/>
				</div>

				<input type="button" value="Valider" name="valider" onclick="resultat();"/>
				<input type="button" value="Reset" onclick="resetEvaluation();" />
			</div>
		</form>			
	</body>
</html>
