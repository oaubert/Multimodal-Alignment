<?php

	session_start();

	if(isset($_POST['valider']))
	{
		$p1 = $_POST['p1'];
		$p2 = $_POST['p2'];
		$p3 = $_POST['p3'];
	
		if(!isset($_SESSION['res']))
		{
			$_SESSION['res'] = $p1 . '-' . $p2 . '-' . $p3;
			$_SESSION['affiche'] = "Slide " . $_SESSION['slide_id'] . " : " . $p1 . ' - ' . $p2 . ' - ' . $p3 . '<br />';
		}
		else
		{
			$_SESSION['res'] = $_SESSION['res'] . ';' . $p1 . '-' . $p2 . '-' . $p3;
			$_SESSION['affiche'] = $_SESSION['affiche'] . "Slide " . $_SESSION['slide_id'] . " : " . $p1 . ' - ' . $p2 . ' - ' . $p3 . '<br />';
		}

		$_SESSION['slide_id'] = $_SESSION['slide_id'] + 1;

		header("Location:index.php?id=" . $_SESSION['slide_id']);
	}
	else
	{
		echo "S'il vous plait, donnez une réponse pour les trois paragraphes.";
	}
?>
