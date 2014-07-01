<!DOCTYPE html>
<html>
    <head>
        <title>Test Alignement Local - Resultat</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<link href="style.css" rel="stylesheet" type="text/css">
    </head>
    <body>
		<p>
			<?php 
				session_start();
				echo 'Fini !<br />'; 
				echo $_SESSION['affiche'];
			?>
		</p>
		<button onclick="location.href='reset.php'">Reset</button>
	</body>
</html>
