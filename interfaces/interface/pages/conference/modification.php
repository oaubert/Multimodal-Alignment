<?php
	session_start();
	if (is_numeric($_GET['id'])){
		$_SESSION['id']=$_GET['id'];
	?>
		<!DOCTYPE html>
		<html>
			<head>
				<title>Test Synchro Txt/Vid</title>
				<meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
				<link href="../../CSS/accueil.css" rel="stylesheet" type="text/css"> 
			</head>
			<body>
				<div id='entete'>
					<h1>TEST DE SYNCHRONISATION</h1>
				</div>
				<div id='choix'>
					<form action='modification_xml.php' method="post">      
						<fieldset>
							<legend> Modification des temps : </legend><br/>
								<p>Temps de début (en s) : <input type="text" name="begin" /></p>
								<p>Temps de fin (en s) : <input type="text" name="end" /></p>
								<p><input type="submit" value="Valider"/></p>
								<div class="precedent"><a href="lecteur.php">Annuler</a></div>
							</legend>
						</fieldset>
					</form>
				</div>
			</body>
		</html>
		<?php
	}
	else {
		header("Location: lecteur.php");
	}
	?>