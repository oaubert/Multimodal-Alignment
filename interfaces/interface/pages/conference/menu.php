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
        ?>
