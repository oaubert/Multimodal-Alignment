<!DOCTYPE html>
<html>
	<head>
		<title>Sélection d'une conférence</title>
		<meta charset="UTF-8" />
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
	<body>
		<fieldset>
			<legend> Sélection d'une conférence </legend>
			<?php
				$chemin="../data";

				$it = new FilesystemIterator($chemin);
	 
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

		<a href="../../index.php"> Menu </a>
	</body>
</html>
