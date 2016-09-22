<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css"/>
 	<link rel="stylesheet" type="text/css" href="css/hours.css" />
 	
 	<!-- jquery must come first and is required by bootstrap -->
	<script src="js/jquery-3.1.0.min.js"></script>
	<script src="js/bootstrap.min.js"></script>

 	<script>
 		$( document ).ready(function() {
 			var target = document.getElementById("target");

 			var readme = target.attributes["data-readme"].value;
 			var updates = target.attributes["data-updates"].value;

 			target.innerHTML = readme + updates;
 		});
 	</script>
</head>

<body>
	
<div class="container" id="viewerContents">
	<div class="row">
		<div class="col-md-8 col-md-offset-2">
			<div class="panel">
				<div class="panel-heading" id="target" data-readme="{{readme}}" data-updates="{{updates}}">
				</div>
			</div>
		</div>
	</div>
</div>

</body>
</html>