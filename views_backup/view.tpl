<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
	<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css"/>
 	<link rel="stylesheet" type="text/css" href="{{ url('static', filename='hours.css') }}" />
</head>


<body>
<div class="container">
	<div class="row">
		<div class="col-md-6 col-md-offset-3">
			<div class="panel panel-default">
				<div class="panel-body">
				% for r in records:
					<p>{{r.emailFormat()}}</p>
				% end
				</div>
			</div>
		</div>
	</div>
</div>	
</body>

</html>