<!DOCTYPE html>
<?php 
	include('../analyseDocument.php');
	include('../function.php');

	if(isset($_GET['id']))
	{
		$_SESSION['slide_id'] = $_GET['id'];
	}
	elseif(!isset($_SESSION['slide_id']))
	{
		header("Location:index.php?id=0");
	}

	if($_SESSION['slide_id'] >= $nbSpeech)
	{
		header("Location:fini.php");
	}

	$max = getMax($_SESSION['slide_id']);
?>
<html>
    <head>
        <title>Test Alignement Local - <?php echo $_SESSION['slide_id']; ?></title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<link href="style.css" rel="stylesheet" type="text/css">
		<script src="script.js"></script>
    </head>
    <body onload="initialisation(<?php timeSpeech($_SESSION['slide_id']); ?>);">

		<video class="drag" width="45%" id="video" height="100%" controls="controls">
			<source src='../Data/video2.webm'>
			<code>video</code>
		</video>

		<div id="controls">
			<button type="button" id="play" onclick="playPause()">Play</button>
			<button type="button" id="replay" onclick="replay()">Replay</button>
		</div>

		<div id="paragraphe">
			Paragraphe 1 : &nbsp;&nbsp;&nbsp;<?php echo $max[0][1]; ?> <div><?php ecrireParagraphe($max[0][0]); ?></div>
			Paragraphe 2 : &nbsp;&nbsp;&nbsp;<?php echo $max[1][1]; ?> <div><?php ecrireParagraphe($max[1][0]); ?></div>
			Paragraphe 3 : &nbsp;&nbsp;&nbsp;<?php echo $max[2][1]; ?> <div><?php ecrireParagraphe($max[2][0]); ?></div>
		</div>

		<form action="traitement.php" method="post">
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

				<input type="submit" value="Valider" name="valider" />
				<input type="button" value="Reset" onclick="location.href='reset.php'");
			</div>
		</form>			
	</body>
</html>
