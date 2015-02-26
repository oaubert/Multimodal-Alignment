<!DOCTYPE html>
<html>
	<head>
		<title>Interface d'évaluation - Sélection d'une conférence</title>
		<meta charset="UTF-8" />
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
	<body>
		<fieldset>
			<legend> Sélection d'une conférence </legend>
			<?php
				$chemin="../data";

				$it = new FilesystemIterator($chemin);

				/** Liste l'ensemble des conférences disponibles : une par dossier présent dans ../data/ 

						Le nom de la conférence est le nom du dossier
						Dans chaque dossier, il peut y avoir un fichier "description" qui contient une phrase de description qui sera affiché à coté
				**/
	 
				foreach($it as $fileinfo)
				{
					if($fileinfo->isDir())
					{
						$description = fopen($fileinfo->getPathname() . '/description', 'r');
						$ligne = fgets($description);

						echo '<a href="visualisation.php?document=' . $fileinfo->getFilename() . '" >' . $fileinfo->getFilename() . '</a>  ' . $ligne . '<br />';

						fclose($description);
					}
				}
			?>
		</fieldset>

		<a href="../../index.html"> Menu </a>
	</body>
</html>
