<!DOCTYPE html>
<html>
	<head>
		<title>Ajouter une conférence</title>
		<meta charset="UTF-8" />
	</head>
	<body>
		<form action='traitement.php' method="post" enctype="multipart/form-data"> 
			<fieldset>
                <legend> Ajout d'une conférence : </legend><br/>
                <label for="nom">Nom de la conférence: </label><input type="text" name="nom" /><br/>
                <label for="pdf">Fichier PDF : </label><input type="file" name="pdf" /><br/>
                <label for="video">Fichier vidéo : </label><input type="file" name="video" /><br/>
                <label for="transcript_v">Fichier transcription video : </label><input type="file" name="transcript_v" /><br/>
				<label for="transcript_s">Fichier transcription slides : </label><input type="file" name="transcript_s" /><br/>
                <label for="nbColonne">Nombre de colonnes par page de l'article: </label>
                <input type="text" id="nbColonne" name="nbColonne" size="8" value="1" onfocus="this.select();"/><br/>
                <input type="submit" value="Envoyer" name="formulaire"/>
				<a href="index.html"><input type="button" value="Retour" name="retour"/></a>
			</fieldset>   
        </form>
	</body>
</html>
