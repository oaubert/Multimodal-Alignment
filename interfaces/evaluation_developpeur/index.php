<!DOCTYPE html>
<?php 
	$chemin = "../data/" . $_GET['document'] . '/';

	if(isset($_GET['id']))
	{
		$_SESSION['slide_id'] = $_GET['id'];
	}
	elseif(!isset($_SESSION['slide_id']))
	{
		header("Location:index.php?id=0");
	}

?>
<html>
    <head>
        <title>Test Alignement Local - <?php echo $_SESSION['slide_id']; ?></title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<link href="style.css" rel="stylesheet" type="text/css">
		<link rel="stylesheet" type="text/css" href="../../js/jquery/css/ui-lightness/jquery-ui-1.10.4.custom.min.css">
		<script type="text/javascript" src="../../js/d3/d3.min.js"></script>
		<script type="text/javascript" src="../../js/jquery/js/jquery-1.10.2.js"></script>
		<script type="text/javascript" src="../../js/jquery/js/jquery-ui.min.js"></script>
		<script type="text/javascript" src="../evaluation/script.js"></script>
    </head>
    <body>

		<div id="data">
			<?php
				include($chemin . "paragraphe.html");
				include($chemin . "speech.html");
				include($chemin . "page.html");
				include($chemin . "alignement.html");
			?>
		</div>

		<script type="text/javascript">
			var idSpeech = "<?php echo $_SESSION['slide_id'] ?>";
			var nbSpeech = d3.select("#data_transcript")[0][0].dataset.number;
			var chemin = "<?php echo $chemin ?>";
			var dataSpeech = d3.selectAll(".data_speech[data-id=\"" + idSpeech + "\"]")[0];
			var dataLink = d3.selectAll(".data_link[data-idspeech=\"" + idSpeech + "\"]")[0];
		</script>

		<div id="transcript">
			Transcript 
			<div id="info_transcript">
				Moyenne : <span id="moyenne"></span><br />
				Écart-type : <span id="ecart_type"></span><br />
				Pourcentage de zéro : <span id="zero"></span>
			</div>
			<div id="text_transcript"></div>
		</div>

		<div id="paragraphe">
			Paragraphe 1 : &nbsp;&nbsp;&nbsp; <span id="similarite1"></span><div id="texte1"></div>
			Paragraphe 2 : &nbsp;&nbsp;&nbsp; <span id="similarite2"></span><div id="texte2"></div>
			Paragraphe 3 : &nbsp;&nbsp;&nbsp; <span id="similarite3"></span><div id="texte3"></div>
		</div>	

		<script type="text/javascript">
			$("#moyenne").html(dataSpeech[0].dataset.moyenne);
			$("#ecart_type").html(dataSpeech[0].dataset.ecart_type);
			$("#zero").html(dataSpeech[0].dataset.zero);
			$("#text_transcript").html(dataSpeech[0].innerHTML);

			afficherParagraphe(0, "similarite1", "texte1");
			afficherParagraphe(1, "similarite2", "texte2");
			afficherParagraphe(2, "similarite3", "texte3"); 
		</script>		
	</body>
</html>
