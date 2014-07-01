<?php

	session_start();

	if(isset($_GET['p']))
	{
		$p = $_GET['p'];
	
		if(!isset($_SESSION['res']))
		{
			$_SESSION['res'] = $p;
			$_SESSION['affiche'] = "Slide " . $_SESSION['slide_id'] . " : " . $p . '<br />';
		}
		else
		{
			$_SESSION['res'] = $_SESSION['res'] . ';' . $p;
			$_SESSION['affiche'] = $_SESSION['affiche'] . "Slide " . $_SESSION['slide_id'] . " : " . $p . '<br />';
		}

		$_SESSION['slide_id'] = $_SESSION['slide_id'] + 1;

		header("Location:index.php?id=" . $_SESSION['slide_id']);
	}
	else
	{
		echo "S'il vous plait, donnez une réponse pour les trois paragraphes.";
	}
?>
