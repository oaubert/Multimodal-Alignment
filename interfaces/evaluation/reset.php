<?php 
	session_start();
	$document = $_SESSION['document'];
	session_unset();
	header("Location:index.php?document=" . $document . "&id=0");
?>
