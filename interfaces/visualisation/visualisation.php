<!DOCTYPE html>
<?php
	$chemin = "../data/" . $_GET['document'] . '/';
?>
<html>
	<head>
		<title>Interface d'évaluation</title>
		<meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
		<link rel="stylesheet" type="text/css" href="style.css">
		<link rel="stylesheet" type="text/css" href="styleInfo.css">
		<link rel="stylesheet" type="text/css" href="../../js/jquery/css/ui-lightness/jquery-ui-1.10.4.custom.min.css">
		<script type="text/javascript" src="../../js/d3/d3.min.js"></script>
		<script type="text/javascript" src="../../js/jquery/js/jquery-1.10.2.js"></script>
		<script type="text/javascript" src="../../js/jquery/js/jquery-ui.min.js"></script>
	</head>
	<body>
		<!-- Menu -->

		<button onclick="location.href='index.php'">Choix des données</button>
		<button onclick="changeMode();">Mode</button>

		<!-- Données -->
		
		<?php
			include($chemin . "paragraphe.html");
			include($chemin . "speech.html");
			include($chemin . "page.html");
			include($chemin . "alignement.html");
		?>
		
			<!-- Sélection des données -->
		<script type="text/javascript">
			var dataParagraphe = d3.selectAll(".data_paragraphe")[0];
			var dataSpeech = d3.selectAll(".data_speech")[0];
			var dataPage = d3.selectAll(".data_page")[0];
			var dataLink = d3.selectAll(".data_link")[0];
			var chemin = "<?php echo $chemin ?>";
			var dureeSpeech = d3.select("#data_transcript")[0][0].dataset.duree;
			var nbSpeech = d3.select("#data_transcript")[0][0].dataset.number;
		</script>


		<!-- Visualisation -->
		<div id="visualisation">
		</div>


		
		<!-- Contrôles -->		

		<div id="controls">
			<label for="out_nbLink">Nombre de liens :</label>
			<input type="range" id="nbLink" min="1" max="20" step="1" value="1" onchange="selectLink(this.value, document.getElementById('seuil').value);" oninput="document.getElementById('out_nbLink').value = value;" />
			<input type="number" id="out_nbLink" min="1" max="20" step="1" value="1" onchange="document.getElementById('nbLink').value = value; selectLink(document.getElementById('nbLink').value, document.getElementById('seuil').value);" />

			<label for="out_seuil">Seuil de similarité :</label>
			<input type="range" id="seuil" min="0" max="1" step="0.01" value="0" onchange="selectLink(document.getElementById('nbLink').value, this.value);" oninput="document.getElementById('out_seuil').value = value;" />
			<input type="number" id="out_seuil" min="0" max="1" step="0.01"  value="0" onchange="document.getElementById('seuil').value = value; selectLink(document.getElementById('nbLink').value, document.getElementById('seuil').value);" />
		</div>



		<!-- Affichage des informations -->

		<div id="affichage">
			<div id="info">
				<div id="info_speech">
				</div>
				<div id="info_paragraphe"></div>
			</div>
			<div id="highligh">
			</div>
		</div>


		<!-- Lancement du script -->
		<script type="text/javascript" src="script.js"></script>
	</body>
</html>
