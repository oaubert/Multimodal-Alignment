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
	$slide = $alignment_dom->getElementById($_SESSION['slide_id']);
?>
<html>
    <head>
        <title>Test Alignement Local - <?php echo $_SESSION['slide_id']; ?></title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<link href="style.css" rel="stylesheet" type="text/css">
    </head>
    <body>

		<div id="transcript">
			Transcript - 
					<?php echo 'Moyenne : ' . round($slide->getAttribute('moyenne'), 5) . ', Ecart-Type : ' . round($slide->getAttribute('ecartType'),5) . "<br />";				
					ecrireTranscript($_SESSION['slide_id']); ?>
		</div>

		<div id="paragraphe">
			<?php
				for($i=0; $i < 3; $i++)
				{
					echo "Paragraphe " . ($i+1) . " : &nbsp;&nbsp;&nbsp;". round($max[$i]->getAttribute('similarite'),5) . " - ";
				 
					foreach(explode(';', $max[$i]->getAttribute('matchingWords')) as $word)
					{
						$w = explode(':', $word);
						ecrireWord($w[0]);
						echo " : " . round($w[1], 3) . ", ";
					}
				
					echo "<div onclick=\"window.location.href = 'traitement.php?p=" . ($i+1) . "';\">";
					ecrireParagraphe($max[$i]->getAttribute('id'));
					echo "</div>";
				}
			?>
		</div>			
	</body>
</html>
