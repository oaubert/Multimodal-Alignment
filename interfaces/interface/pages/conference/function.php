<?php
	$directory = $chemin.'/';
            if (is_dir($directory)) {
              if ($dh = opendir($directory)) {
                while (($file = readdir($dh)) !== false) {
                  if($file!='..' && $file!='.'){//N'affiche pas le . et ..
                      $extension = strrchr($file, '.');
                      if($extension == '.pdf'){
                          $pdf = $file;
                      }
                      elseif($extension == '.xml'){
                          $xml = $file;
                      }
                      elseif($extension == '.webm' || $extension == '.mp4'){
                          $video = $file;
                      }
                  }
                }
                closedir($dh); //Il est vivement conseillé de fermer le repertoire pour toute autre opération sur le systeme de fichier.
              }
            }

	function chargerDocument($editer)
	{
		global $chemin, $xml, $pdf, $video;

		$dom=new DOMDocument();
		
        if($editer){
            $dom->load($chemin.'/editer/'.$xml);
        }
        else{
            $dom->load($chemin.'/'.$xml);
        }
        $racine=$dom->documentElement;
        
        $pages=$racine->getElementsByTagName('page');
        $id = 0;
        foreach($pages as $page) {
            echo "<div style=\"position:relative;\" width='100%' height='100%' display='inline'>";
            foreach($page->childNodes as $para) {
                if($para->nodeName=='texte') {//href ='#".$id."'
                    if($editer){
                        echo "<a id='".$id."' ondblclick='ModificationSynchronisation(".$id.")' onClick='SynchroniseVideo(".$id.")' ";
                        echo "time='".$para->getAttribute('time')."' ";
                        echo "style='position:absolute; ".$para->getAttribute('style')." z-index:1;' ";
                        echo "title='".$para->getAttribute('time')."' ";
                        echo "onmouseout=\"this.style.background='rgba(0, 0, 0, 0)';\" onmouseover=\"this.style.background='rgba(4, 133, 157, 0.15)';\">";
                        echo "</a>";
                    }
                    else{
                        echo "<a id='".$id."' onClick='SynchroniseVideo(".$id.")' time='".$para->getAttribute('time')."' ";
                        echo "style='position:absolute; ".$para->getAttribute('style')." z-index:1;' ";
                        echo "title='".$para->getAttribute('time')."' ";
                        echo "onmouseout=\"this.style.background='rgba(0, 0, 0, 0)';\" onmouseover=\"this.style.background='rgba(4, 133, 157, 0.15)';\">";
                        echo "</a>";
                    }
                    $id++;
                }
            }
            echo "<img src='".$chemin."/img/PICTURE_".$page->getAttribute('numero').".jpg' style='position:relative; top:0px; left:0px;' width='100%'/></div>";
		}
	}
?>
