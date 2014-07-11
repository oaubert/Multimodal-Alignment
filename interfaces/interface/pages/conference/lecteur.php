<?php 
	$chemin = "../../../data/" . $_GET['document'] . '/';
?>
<!DOCTYPE html>
<html>
    <head>
        <title>Test Synchro Txt/Vid</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
        <script src="../../../../js/jquery/js/jquery-1.10.2.js"></script>
		<script src="../../../../js/jquery/js/jquery-ui-1.10.4.custom.js"></script>
        <script src="../../JAVASCRIPT/popcorn.js"></script>
        <script src="../../JAVASCRIPT/synchronisation.js"></script>	
        <script src="../../JAVASCRIPT/progressbar_mini.js"></script>
		<script type="text/javascript" src="../../../../js/d3/d3.min.js"></script>
		<script type="text/javascript" src="script.js"></script>
        <link href="../../../../js/jquery/css/ui-lightness/jquery-ui-1.10.4.custom.css" rel="stylesheet" type="text/css">
        <link href="../../CSS/Synchro.css" rel="stylesheet" type="text/css"> 
		<link href="../../CSS/Editor.css" rel="stylesheet" type="text/css">  
    </head>
    <body onLoad="initialisation(ourvideo, 50, false);">
		<div id="data">
			<?php 
				include($chemin . "paragraphe.html");
				include($chemin . "speech.html");
				include($chemin . "page.html");
				include($chemin . "alignement.html");
			?>
		</div>

		<div id='entete'>
			<h1>TEST DE SYNCHRONISATION</h1>
		</div>
		<div id="accueil">
				<div class="boutons"><a href="../accueil/accueil.php">Accueil</a></div>	
                <div class="boutons"><a href="editer.php">Editer</a></div>	
		</div>
		<div id='milieu'>
			<div id='video'>
				<!-- Affichage de la vidéo -->
				<video onmousedown='DebutModificationTailleVideo(event)' class="drag" width="100%" id="ourvideo">
					<?php echo '<source src=\''.$chemin.'video.webm\'>'; ?> 
					<code>video</code>
				</video>
			</div>
			<div id="texte" width='100%'>
			<table height='100%' width='100%' cellspacing='0px' cellpadding='0px'>
				<tr>
					<td valign='center' width='49%' id="tdTexte">
					</td>
				</tr>
			</table >
			</div>
		</div>
        <div id="video_controller">
			<table align='center' >
				<tr>
					<td>
						<a id="btn_play"><img src="../../IMAGE_boutons/play.png" /></a>
					</td>
					<td>
						<div id="timeline"></div>
					</td>
					<td>
						<a id="btn_mute"><img src="../../IMAGE_boutons/volume.png" /></a>
					</td>
					<td>
						<input type="range" min="0" max="1" step="0.01" id="volume">
					</td>
					<td>
						<label id="time">-:--:--</label>
					</td>
					<td>
						<input type="checkbox" id='btn_active'>activer synchro </input>
					</td>
				</tr>
			</table>
        </div>
		<div id='lien_pdf' >
			<a top='10px' onclick="window.open('<?php echo $chemin.'/paper.pdf'; ?>');" onmouseover="" style="cursor: pointer;">Lien de téléchargement du pdf</a>
		</div>
        
		<script type="text/javascript">
			var dataParagraphe = d3.selectAll(".data_paragraphe")[0];
			var dataSpeech = d3.selectAll(".data_speech")[0];
			var dataPage = d3.selectAll(".data_page")[0];
			var dataLink = d3.selectAll(".data_link")[0];
			var chemin = "<?php echo $chemin; ?>";

			chargerDocument();	
		</script>       
 
    </body>
</html>
