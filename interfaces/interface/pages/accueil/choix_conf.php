<?php
session_start();
if (isset($_POST['conference']) && !empty($_POST['conference'])){
	$_SESSION['conference']=$_POST['conference'];
	header("Location: ../conference/lecteur.php");
	}
else {
	header("Location: accueil.php");
}
?>