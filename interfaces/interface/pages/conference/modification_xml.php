<?php
	session_start();
	if (is_numeric($_GET['id'])){
		$_SESSION['id']=$_GET['id'];
	

        $chemin = $_SESSION['conference'];
        $directory = '../conference/'.$chemin.'/editer/';
        if (is_dir($directory)) {
              if ($dh = opendir($directory)) {
                while (($file = readdir($dh)) !== false) {
                  if($file!='..' && $file!='.'){//N'affiche pas le . et ..
                      $extension = strrchr($file, '.');
                      if($extension == '.xml'){
                          $xml = $file;
                      }
                  }
                }
                closedir($dh); //Il est vivement conseillé de fermer le repertoire pour toute autre opération sur le systeme de fichier.
              }
            }
		$dom = new DOMDocument();
		$dom->load($chemin.'/editer/'.$xml);
		$liste_temps = $dom->documentElement;
		$temps = $liste_temps->getElementsByTagName('texte');
	
		foreach($temps as $time)
		{
			if($time->getAttribute('id')==$_SESSION['id'])
			{
				$time->setAttribute("time",$_GET['begin']."_".$_GET['end']);
			}
		}
	
		if(($_GET['begin'] > 0)&&($_GET['end'] > 0)&&($_GET['begin'] < $_GET['end'])&&(is_numeric($_GET['begin']))&&(is_numeric($_GET['end']))){
		  $dom->save($chemin.'/editer/'.$xml);
		}
	}

	header("Location: lecteur.php"/*.$_SESSION['conference'].""*/);
?>
