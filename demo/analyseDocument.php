<?php 

	session_start();

	$chemin = "../data/" . $_GET['document'] . '/';

	$transcript_dom = new DOMDocument();
	$transcript_dom->load($chemin . 'transcript.xml');
	$transcript_racine = $transcript_dom->documentElement;

	$pdf_dom = new DOMDocument();
	$pdf_dom->load($chemin . 'pdf.xml');
	$pdf_racine = $pdf_dom->documentElement;

	$alignment_dom = new DOMDocument();
	$alignment_dom->load($chemin . 'alignment.xml');
	$alignment_racine = $alignment_dom->documentElement;

	$page_dom=new DOMDocument();
	$page_dom->load($chemin . 'page.xml');
	$page_racine=$page_dom->documentElement;

	$vocabulary_dom=new DOMDocument();
	$vocabulary_dom->load($chemin . 'vocabulary.xml');
	$vocabulary_racine=$vocabulary_dom->documentElement;

	$infoSpeech_dom=new DOMDocument();
	$infoSpeech_dom->load($chemin . 'infoSpeech.xml');
	$infoSpeech_racine=$infoSpeech_dom->documentElement;

	$infoParagraphe_dom=new DOMDocument();
	$infoParagraphe_dom->load($chemin . 'infoParagraphe.xml');
	$infoParagraphe_racine=$infoParagraphe_dom->documentElement;




	$pages=$page_racine->getElementsByTagName('page');
	$afficheParagraphe = $page_racine->getElementsByTagName('texte');

	$nbSpeech = $transcript_racine->getAttribute('nbSpeech');
	$nbParagraphe = $pdf_racine->getAttribute('nbParagraphe');
	$duree = $transcript_racine->getAttribute('duree');

	$speech = $transcript_racine->getElementsByTagName('speech');
	$paragraphe = $pdf_racine->getElementsByTagName('paragraphe');
	$alignment = $alignment_racine->getElementsByTagName('speech');
	$vocabulary = $vocabulary_racine->getElementsByTagName('word');
	$infoSpeech = $infoSpeech_racine->getElementsByTagName('speech');
	$infoParagraphe = $infoParagraphe_racine->getElementsByTagName('paragraphe');

	foreach($paragraphe as $p)
	{
		$p->setIdAttribute('id', true);
	}

	foreach($speech as $s)
	{
		$s->setIdAttribute('id', true);
	}

	foreach($alignment as $a)
	{
		$a->setIdAttribute('id', true);
	}

	foreach($vocabulary as $word)
	{
		$word->setIdAttribute('id', true);
	}

	foreach($infoSpeech as $s)
	{
		$s->setIdAttribute('id', true);
	}

	foreach($infoParagraphe as $s)
	{
		$s->setIdAttribute('id', true);
	}

?>
