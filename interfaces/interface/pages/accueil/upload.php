<!DOCTYPE html>
<html>
    <head>
        <title>Projet Synchronisation Texte/Vidéo</title>
        <meta http-equiv="Content-Type" content="text/html;"> 
        <link href="../../CSS/accueil.css" rel="stylesheet" type="text/css"> 
    </head>
    <body>
	<div id='entete'>
            <h1>Projet : Synchronisation Texte/Vidéo</h1>
	</div>
	<div id='choix'>
            <?php
                /* Cette fonction s'execute seulement si le formulaire à été validé.
                 * Elle permet de placer un pdf et une video dans le dossier /pages/conference/[nom du pdf]
                 * De plus, elle crée dans ce dossier, un dossier images afin de pouvoir executer le .jar
                 * Qui nous permet de crée le fichier xml.
                 * Enfin, elle place aussi le fichier php de base dans ce dossier.
                 */
            	if(isset($_POST['formulaire']))
				{
					$arg['nbColonne'] = 1;
                    $arg['pdf'] = null;
                    $arg['xml'] = null;
                    $arg['video'] = null;
                    $arg['images'] = null;

                    $nomdossier = htmlspecialchars($_POST['nom']);

                    $arg['nbColonne'] = htmlspecialchars($_POST['nbColonne']);

					echo $arg['nbColonne'];

                    if(isset($_FILES['pdf']) && isset($_FILES['video']))
					{
                        $extensionsVideo = array('.mp4', '.webm');
                        $extensionPDF = strrchr($_FILES['pdf']['name'], '.');
                        $extensionVideo = strrchr($_FILES['video']['name'], '.');
                        
						if(isset($_FILES['xml']))
						{
                            $extensionXml = strrchr($_FILES['xml']['name'], '.');
                            $arg['xml'] = $_FILES['xml']['name'];
                        }
                        else
						{
                            $extensionXml = null;
                        }

                        if($extensionPDF == '.pdf' && in_array($extensionVideo, $extensionsVideo))
						{
                            $dossier = '../conference/';
                            
                            if(empty($nomdossier)){
                                $nomdossier = basename($_FILES['pdf']['name'], '.pdf'); 
                            }    
                            
                            if(mkdir($dossier.$nomdossier))
							{ 
                                $dossier = $dossier.$nomdossier;

                                if(move_uploaded_file($_FILES['pdf']['tmp_name'], $dossier.'/'.$_FILES['pdf']['name']))
								{
                                	$arg['pdf'] = $dossier."/".$_FILES['pdf']['name'];

	                                if(move_uploaded_file($_FILES['video']['tmp_name'], $dossier.'/'.$_FILES['video']['name']))
									{
			       						$arg['video'] = $dossier."/".$_FILES['video']['name'];
                                       	if(mkdir($dossier.'/img'))
										{
					   						$arg['images'] = $dossier;
                                           	if(mkdir($dossier.'/editer'))
											{
                                            	if($extensionXml == '.xml')
												{
                                                	if(move_uploaded_file($_FILES['xml']['tmp_name'], $_FILES['xml']['name']))
													{
                                                        $err = 0;
                                                    }
                                                    else
													{
                                                        $err = 1;
														echo 'Erreur xml';
                                                    }
                                                }
                                                else
												{                                                    
                                                    $err = 0;
                                                }
                                           	}
                                       		else
											{
												echo 'Erreur editer';
                                                $err = 1;
                                           	}
                                       	}
                                       	else
										{
											echo 'Erreur img';
                                            $err = 1;
                                       	}
                                   	}
                                   	else
									{
										echo'Erreur mv_video';
                                       	$err = 1;
                                   	}
                            	}
                                else
								{
									echo 'Erreur mv_pdf';
                                    $err = 1;
                                }
                    		}
                            else
							{
								echo 'Erreur mkdir';
                                $err = 1;
                            }
                    	}
                        else
						{
                            $err = 2;
                        }
                    }
                    else
					{
                        $err = 3;
                    }

                    /* Gestion des erreurs : */
                    if($err == 0)
					{
						echo "Lancement du script bash<br />";
						$parametres = $arg['pdf']." ".$arg['images']." ".$arg['nbColonne'];
						shell_exec("./pdf.sh ".$parametres." ".$arg['xml']." 2> err.log > normal.log");
                        echo '<font color=\'green\'>Fichiers ajoutés avec succès</font>';
                    }
                    elseif($err == 1)
					{
                        echo '<font color=\'red\'>Erreur a la création des fichiers</font>';
                    }
                    elseif($err == 2)
					{
                        echo '<font color=\'red\'>Video: .webm | .mp4 // PDF: .pdf</font>';
                    }
                    elseif($err == 3)
					{
                        echo '<font color=\'red\'>Vous devez importer une vidéo et un pdf</font>';
                    }
                }
 
            ?>
            <form action='upload.php' method="post" enctype="multipart/form-data"> 
				<fieldset>
                    <legend> Upload des fichiers : </legend><br/>
                    <label for="nom">Nom de la conférence: </label><input type="text" name="nom" /><br/>
                    <label for="pdf">Fichier PDF : </label><input type="file" name="pdf" /><br/>
                    <label for="video">Fichier vidéo : </label><input type="file" name="video" /><br/>
                    <label for="xml">Fichier XML (facultatif) : </label><input type="file" name="xml" /><br/>
                    <label for="nbColonne">Nombre de colonnes par page : </label>
                    <input type="text" id="nbColonne" name="nbColonne" size="8" value="1" onfocus="this.select();"/><br/>
                    <input type="submit" value="Envoyer" name="formulaire"/>
 				</fieldset>   
            </form>
            <div class="precedent"><a href="accueil.php">Accueil</a></div>
	</div>
    </body>
</html>
	
