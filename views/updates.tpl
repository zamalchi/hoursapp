<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
	<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css"/>
 	<link rel="stylesheet" type="text/css" href="{{ url('static', filename='hours.css') }}" />
</head>

<body>
	
<div class="container" id="viewerContents">
	<div class="row">
		<div class="col-md-8 col-md-offset-2">
			<div class="panel">
				<div class="panel-heading">
					% if type(updates) is str:
						<h4>{{updates}}</h4>
		
					% else:
						<h4>Updates:</h4>

						<ol>
						% for u in updates:
							<li>
								% if "BUGFIX" in u:
									<span class="bugfix">BUGFIX</span> {{u.split("BUGFIX")[1]}}
								% else:
									{{u}}
								% end
							</li>
						% end
						</ol>
					% end
				</div>
			</div>
		</div>
	</div>
</div>

</body>
</html>