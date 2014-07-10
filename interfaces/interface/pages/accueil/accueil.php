<!DOCTYPE html>
<html>
    <head>
        <title>Projet Synchronisation Texte/Vid√©o</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
		<link href="../../CSS/accueil.css" rel="stylesheet" type="text/css"> 
	</head>
	<body>
		<div id='entete'>
			<h1>Projet : Synchronisation Texte/Vid√©o</h1>
		</div>
		<div id='choix'>
                
			<form action='choix_conf.php' method="post">      
				<fieldset>
					<legend> Choix de la conf√©rence : </legend><br/>
					
						<label id='conference' for="conf√©rence">Titre de la conf√©rence : </label>
						<select name='conference' size='1' id='conference'>
                                                    <?php
                                                        /* Ici, on rÈcupËre le nom de tous les dossiers prÈsents dans le dossier
                                                         * /pages/conference, afin de crÈer les liens dans le formulaire vers 
                                                         * les diffÈrentes pages de confÈrence
                                                         */
                                                        $directory = '../../../data/';
                                                        if (is_dir($directory)) {
                                                          if ($dh = opendir($directory)) {
                                                            while (($file = readdir($dh)) !== false) {
                                                              if($file!='..' && $file!='.' && $file!='modification_xml.php' && $file!='lecteur.php' && $file!='modification.php' && $file!='function.php' && $file!='menu.php' && $file!='editer.php'){//N'affiche pas le . et ..
                                                                echo "<option value=\"".$file."\">".$file."</option>";
                                                              }
                                                            }
                                                            closedir($dh); //Il est vivement conseillÈ de fermer le repertoire pour toute autre opÈration sur le systeme de fichier.
                                                          }
                                                        }
                                                    ?>

						</select>
						<div id='valider'>
						<input name="go" type="submit" title="Envoyer le message" />  
						</div>
                                                
				</fieldset>   
			</form>
                    <div class="precedent"><a href="upload.php">Upload</a></div>
		</div>
	</body>
</html>
	
