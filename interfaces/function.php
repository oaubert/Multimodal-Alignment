<?php 
	
	function cmp($node1, $node2)
	{
		$sim1 = $node1->getAttribute('similarite');
		$sim2 = $node2->getAttribute('similarite');

		if($sim1 == $sim2)
		{
			return 0;
		}
		elseif($sim1 > $sim2) #inverse pour équivalent rsort()
		{
			return -1;
		}
		else
		{
			return 1;
		}
	}

	function getMax($id_slide)
	{
		global $alignment_dom;
		$paragraphe_linked = $alignment_dom->getElementById($id_slide)->getElementsByTagName('paragraphe');
		
		$array = array();
		
		foreach($paragraphe_linked as $p)
		{
			array_push($array, $p);
		}

		usort($array, "cmp");

		return $array;
	}

	function ecrireParagraphe($id)
	{
		global $pdf_dom;
		echo $pdf_dom->getElementById($id)->nodeValue;
	}

	function stringParagraphe($id)
	{
		global $pdf_dom;
		return $pdf_dom->getElementById($id)->nodeValue;
	}

	function ecrireTranscript($id)
	{
		global $transcript_dom;
		echo $transcript_dom->getElementById($id)->nodeValue;
	}

	function stringTranscript($id)
	{
		global $transcript_dom;
		return $transcript_dom->getElementById($id)->nodeValue;
	}

	function ecrireWord($id)
	{
		global $vocabulary_dom;
		echo $vocabulary_dom->getElementById($id)->nodeValue;
	}

	function stringWord($id)
	{
		global $vocabulary_dom;
		return $vocabulary_dom->getElementById($id)->nodeValue;
	}

	function getWordInfo($id)
	{
		global $vocabulary_dom;
		$word = $vocabulary_dom->getElementById($id);
		$info = array();
		$info['value'] = $word->nodeValue;
		$info['df'] = $word->getAttribute('df');
		$info['idf'] = $word->getAttribute('idf');
		
		return $info;
	}

	function getWordInfoInParagraphe($idWord, $idParagraphe)
	{
		global $infoParagraphe_dom;
		$paragraphe = $infoParagraphe_dom->getElementById($idParagraphe);
		$info = getWordInfo($idWord);

		$find = false;

		foreach($paragraphe as $word)
		{
			if($word->getAttribute('idWord') == $idWord)
			{
				$info['tf'] = $word->getAttribute('tf');
				$info['tf_base'] = $word->getAttribute('tf_base');
				$info['tfidf'] = $word->getAttribute('tfidf');
				$find = true;
				break;
			}
		}

		if($find)
		{
			$info['tf'] = 0;
			$info['tf_base'] = 0;
			$info['tfidf'] = 0;
		}

		return $info;
	}


	function getWordInfoInTranscript($idWord, $idSpeech)
	{
		global $infoSpeech_dom;
		$speech = $infoSpeech_dom->getElementById($idSpeech);
		$info = getWordInfo($idWord);

		$find = false;

		foreach($speech as $word)
		{
			if($word->getAttribute('idWord') == $idWord)
			{
				$info['tf'] = $word->getAttribute('tf');
				$info['tf_base'] = $word->getAttribute('tf_base');
				$info['tfidf'] = $word->getAttribute('tfidf');
				$find = true;
				break;
			}
		}

		if($find)
		{
			$info['tf'] = 0;
			$info['tf_base'] = 0;
			$info['tfidf'] = 0;
		}

		return $info;
	}
		

	function timeSpeech($id)
	{
		global $transcript_dom;
		$debut = $transcript_dom->getElementById($id)->getAttribute('begin');
		$fin = $transcript_dom->getElementById($id)->getAttribute('end');
		echo $debut . ', ' . $fin;
	}

	function getMatchingWords($slide_id)
	{
		global $alignment_dom;
		$str_matchingWords = $alignment_dom->getElementById($slide_id)->getAttribute('matchingWords');

		$array_matchingWords = array_map(
								function($a) { return explode(',', $a); },
								 explode(';', $str_matchingWords));
		
		return $array_matchingWords;
	}






	function getInfoParagraphe($paragraphe)
	{
		$info = array();
		$info["matchingWords"] = array();

		foreach(explode(';', $paragraphe->getAttribute('matchingWords')) as $word)
		{
			$w = explode(':', $word);

			$info["matchingWords"][$w[0]] = $w[1];
		}

		
	
	}


	function findOriginalWord($word)
	{}




	//Fonction honteusement copiée, puis modifiée: www.php.net/manual/fr/function.str-ireplace.php, contribution de sawdust
	function highlightStr($haystack, $needle, $id, $value, $color) {
		 // return $haystack if there is no highlight color or strings given, nothing to do.
		if (strlen($haystack) < 1 || strlen($needle) < 1 || strlen($color) < 1) {
		    return $haystack;
		}
		preg_match_all("/$needle/i", $haystack, $matches);
		if (is_array($matches[0]) && count($matches[0]) >= 1) {
		    foreach ($matches[0] as $match) {
				$haystack = preg_replace("/(\s$match\s)|(\s$match$)|(^$match\s)|(^$match$)/i", " <abbr title='".$value."' style='background-color:".$color."' onclick='$(\"#highligh\").load(\"affiche.php?type=word&id=" . $id ."\");'>".$match."</abbr> ", $haystack);
		    }
		}
		return $haystack;
	}


?>
