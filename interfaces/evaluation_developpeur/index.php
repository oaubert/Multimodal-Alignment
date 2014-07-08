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

			var link1 = dataLink[0];
			var link2 = dataLink[1];
			var link3 = dataLink[2];

			var paragraphe1 = $(".data_paragraphe[data-id=\"" + link1.dataset.idparagraphe + "\"]");
			var paragraphe2 = $(".data_paragraphe[data-id=\"" + link2.dataset.idparagraphe + "\"]");
			var paragraphe3 = $(".data_paragraphe[data-id=\"" + link3.dataset.idparagraphe + "\"]");
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
			Paragraphe 1 : 
				<div id="info_paragraphe1">
					Similarité : <span id="similarite1"></span><br />
					Matching words : <span id="matching_words1"></span>
				</div>
				<div id="texte1"></div>
			Paragraphe 2 : 
				<div id="info_paragraphe2">
					Similarité : <span id="similarite2"></span><br />
					Matching words : <span id="matching_words2"></span>
				</div>
				<div id="texte2"></div>
			Paragraphe 3 : 
				<div id="info_paragraphe3">
					Similarité : <span id="similarite3"></span><br />
					Matching words : <span id="matching_words3"></span>
				</div>
				<div id="texte3"></div>
		</div>	

		<script type="text/javascript">
			$("#moyenne").html(dataSpeech[0].dataset.moyenne);
			$("#ecart_type").html(dataSpeech[0].dataset.ecart_type);
			$("#zero").html(dataSpeech[0].dataset.zero);
			$("#text_transcript").html(dataSpeech[0].innerHTML);

			$("#similarite1").html(link1.dataset.similarite);
			$("#matching_words1").html(link1.innerHTML);
			$("#texte1").html(paragraphe1.html());

			$("#similarite2").html(link2.dataset.similarite);
			$("#matching_words2").html(link2.innerHTML);
			$("#texte2").html(paragraphe2.html());

			$("#similarite3").html(link3.dataset.similarite);
			$("#matching_words3").html(link3.innerHTML);
			$("#texte3").html(paragraphe3.html());
		</script>		
	</body>
</html>
