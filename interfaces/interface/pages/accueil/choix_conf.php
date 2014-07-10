<?php
if (isset($_POST['conference']) && !empty($_POST['conference'])){
	header("Location: ../conference/lecteur.php?document=" . $_POST['conference']);
	}
else {
	header("Location: accueil.php");
}
?>
