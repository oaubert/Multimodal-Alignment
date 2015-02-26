<!DOCTYPE html>
<html>
    <head>
        <title>Projet Synchronisation Texte/Vidéo</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
		<link href="../../CSS/accueil.css" rel="stylesheet" type="text/css"> 
	</head>
	<body>
		<div id='entete'>
			<h1>Projet : Synchronisation Texte/Vidéo</h1>
		</div>
		<div id='choix'>
                
                            <ul>
                                                    <?php
                                                        /* Ici, on r�cup�re le nom de tous les dossiers pr�sents dans le dossier
                                                         * /pages/conference, afin de cr�er les liens dans le formulaire vers 
                                                         * les diff�rentes pages de conf�rence
                                                         */
                                                        $directory = '../conference/';
                                                        if (is_dir($directory)) {
                                                          if ($dh = opendir($directory)) {
                                                            while (($file = readdir($dh)) !== false) {
                                                              if($file!='..' && $file!='.' && $file!='modification_xml.php' && $file!='lecteur.php' && $file!='modification.php' && $file!='function.php' && $file!='menu.php' && $file!='editer.php'){//N'affiche pas le . et ..
                                                                echo "<li><a href='../conference/lecteur.php?conference=$file'>$file</a></li>";
                                                              }
                                                            }
                                                            closedir($dh); //Il est vivement conseill� de fermer le repertoire pour toute autre op�ration sur le systeme de fichier.
                                                          }
                                                        }
                                                    ?>

						</select>
						</div>
                                                
				</fieldset>   
                    <div class="precedent"><a href="upload.php">Upload</a></div>
		</div>
	</body>
</html>
	
