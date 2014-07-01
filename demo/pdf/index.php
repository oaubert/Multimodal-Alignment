<!DOCTYPE html>
<?php
	include("../analyseDocument.php");
	include("../function.php");
	include("../create.php");

	$num_page = $_GET['page'];
?>
<html>
	<head>
		<title>Tests D3js</title>
		<meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
        <meta name="description" content="">
		<link rel="stylesheet" type="text/css" href="style.css">
		<link rel="stylesheet" type="text/css" href="styleInfo.css">
		<link rel="stylesheet" type="text/css" href="../visualisation/jquery/css/ui-lightness/jquery-ui-1.10.4.custom.min.css">
		<script type="text/javascript" src="../visualisation/d3/d3.min.js"></script>
		<script type="text/javascript" src="../visualsiation/jquery/js/jquery-1.10.2.js"></script>
		<script type="text/javascript" src="../visualisation/jquery/js/jquery-ui.min.js"></script>
	</head>
	<body>
		<div id="visualisation">
		</div>
		<?php echo '
		<script type="text/javascript">
			var documentName = "' . $_GET['document'] . '";

			var num_page = ' . $num_page . ';			

			var dataPage = new Array();

			var dataParagraphe = new Array(); //HG, HD, BD, BG
			
				';

				$id = 0;
				$id_page = 0;

				foreach($pages as $page)
				{
					$size = getimagesize($chemin . 'img/PICTURE_' . ($id_page+1) . '.jpg');

					echo '
				
				dataPage[' . $id_page . '] = {"id" : ' . $id_page . ', "src" : "' . $chemin . 'img/PICTURE_' . ($id_page+1) . '.jpg", "x" : ' . ((int)($id_page%11)*130+30) . ', "y" : ' . ((int)($id_page/11)*170 + 250) . ', "width" : ' . $size[0] . ', "height" : ' . $size[1] . '};

				';


					if($id_page == $num_page)
					{	
						foreach($page->childNodes as $para)
						{
							if($para->nodeName=='texte') 
							{
								$style = explode('%;', $para->getAttribute('style'));
								$top = substr($style[0], 4);
								$left = substr($style[1], 6);
								$right = substr($style[2], 7);
								$bottom = substr($style[3], 8);

								echo 'dataParagraphe[' . $id . '] = {"id" : ' . $id . ', "page" : ' . $id_page . ', "data" : [{"x":' . $left . ', "y":' . $top .'},
																			  {"x":' . (100-$right) . ', "y":' . $top .'},
																			  {"x":' . (100-$right) . ', "y":' . (100-$bottom) .'},
																			  {"x":' . $left .', "y":' . (100-$bottom) . '}]};
				';	
						
								$id++;
							}
						}
					}

					$id_page++;

				}

		echo '
		</script>'; ?>

		<script type="text/javascript" src="script.js"></script>
	</body>
</html>
