<?php 
session_start();
$chemin = $_GET['conference'];
?>
<!DOCTYPE html>
<html>
    <head>
        <title>Test Synchro Txt/Vid</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
        <script src="../../JAVASCRIPT/jquery-ui/js/jquery-1.10.2.js"></script>
		<script src="../../JAVASCRIPT/jquery-ui/js/jquery-ui-1.10.4.custom.js"></script>
        <script src="../../JAVASCRIPT/popcorn.js"></script>
        <script src="../../JAVASCRIPT/synchronisation.js"></script>	
        <script src="../../JAVASCRIPT/progressbar_mini.js"></script>
        <link href="../../JAVASCRIPT/jquery-ui/css/ui-lightness/jquery-ui-1.10.4.custom.css" rel="stylesheet" type="text/css">
        <link href="../../CSS/Synchro.css" rel="stylesheet" type="text/css"> 
		<link href="../../CSS/Editor.css" rel="stylesheet" type="text/css">  
    </head>
    <body onLoad="initialisation(ourvideo, 50, false);">
		<?php include 'function.php'; ?>
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
					<?php echo '<source src=\''.$chemin.'/'.$video.'\'>'; ?> 
					<code>video</code>
				</video>
			</div>
			<div id="texte" width='100%'>
			<table height='100%' width='100%' cellspacing='0px' cellpadding='0px'>
				<tr>
					<td valign='center' width='49%' id="tdTexte">
                        <?php
                            chargerDocument(false);
                        ?>
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
						<input checked="" type="checkbox" id='btn_active'>activer synchro </input>
					</td>
				</tr>
			</table>
        </div>
		<div id='lien_pdf' >
			<a top='10px' onclick="window.open('<?php echo $chemin.'/'.$pdf; ?>');" onmouseover="" style="cursor: pointer;">Lien de telechargement du pdf</a>
		</div>
        <!-- Version Test
        Cette liste doit être généré par code javascript -->

        
    </body>
</html>
