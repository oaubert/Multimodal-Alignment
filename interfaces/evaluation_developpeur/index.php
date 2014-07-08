<!DOCTYPE html>
<?php 
	$chemin = "../data/" . $_GET['document'] . '/';
?>
<html>
    <head>
        <title>Test Alignement Local</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<link href="style.css" rel="stylesheet" type="text/css">
		<link rel="stylesheet" type="text/css" href="../../js/jquery/css/ui-lightness/jquery-ui-1.10.4.custom.min.css">
		<script type="text/javascript" src="../../js/d3/d3.min.js"></script>
		<script type="text/javascript" src="../../js/jquery/js/jquery-1.10.2.js"></script>
		<script type="text/javascript" src="../../js/jquery/js/jquery-ui.min.js"></script>
		<script type="text/javascript" src="script.js"></script>
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
			<div id="paragraphe1">
				Paragraphe 1 : 
					<div id="info_paragraphe1">
						Similarité : <span id="similarite1"></span><br />
						Matching words : <span id="matching_words1"></span>
					</div>
					<div id="texte1"></div>
			</div>
			<div id="paragraphe2">
				Paragraphe 2 : 
					<div id="info_paragraphe2">
						Similarité : <span id="similarite2"></span><br />
						Matching words : <span id="matching_words2"></span>
					</div>
					<div id="texte2"></div>
			</div>
			<div id="paragraphe3">
				Paragraphe 3 : 
					<div id="info_paragraphe3">
						Similarité : <span id="similarite3"></span><br />
						Matching words : <span id="matching_words3"></span>
					</div>
					<div id="texte3"></div>
			</div>
		</div>	

		<script type="text/javascript">
			var idSpeech = 0;
			var nbSpeech = d3.select("#data_transcript")[0][0].dataset.number;
			var chemin = "<?php echo $chemin ?>";

			afficherTranscript(idSpeech);
		</script>		
	</body>
</html>
