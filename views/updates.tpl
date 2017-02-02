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
 			var heading = document.getElementById("target-heading");
 			var body = document.getElementById("target-body")

 			var readme = heading.attributes["data-readme"].value;
 			var updates = body.attributes["data-updates"].value;

 			heading.innerHTML += readme;
 			body.innerHTML = updates;
 		});
 	</script>
</head>

<body name="top">
	
<div class="container-fluid" id="viewerContents">
	<div class="row">
		<div class="col-md-8 col-md-offset-2">
			<div class="panel" id="help">
				<div class="panel-heading" id="target-heading" data-readme="{{readme}}">
					<center>
					<h2>
						<a href="https://github.com/zamalchi/hoursapp.git">hours</a> : bottle app for recording hours worked
					</h2>
					</center>

					<center>
					<h4>
						<a href="#updates">**UPDATES**</a> -
						<a href="#running"> running </a> -
						<a href="#installation"> installation </a> -
						<a href="#usage"> usage </a> -
						<a href="#remote-host-logging"> remote host logging </a> -
						<a href="#misc"> misc </a>
					</h4>
					</center>
				</div>
				<hr>
				<div class="panel-body" id="target-body" data-updates="{{updates}}"></div>
			</div>
		</div>
	</div>
</div>

</body>
</html>