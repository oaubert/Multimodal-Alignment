<!DOCTYPE html>
<?php 
	include('../analyseDocument.php');
	include('../function.php');
?>
<html>
    <head>
        <title>Vocabulaire</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<link href="style.css" rel="stylesheet" type="text/css">
    </head>
    <body>
		<?php 
				echo $_GET['id'];
				echo $vocabulary->getElementById($_GET['id']); 
		?>
	</body>
</html>
