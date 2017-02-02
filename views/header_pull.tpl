<%
""" POST /pull
Provides values that are set to the name and date cookies
Redirects to GET /hours and pulls any existing records on file
	corresponding to the cookie values
name : required, uses existing cookie for the default value
date : not required, but defaults internally to the current date
"""
%>
<form action="/pull" method="post" enctype="multipart/form-data">
	
	<div name="inputs">
		
		<!-- NAME : TEXT -->
		<input type="text" name="name" id="setName" class="form-control input-sm"
			value="{{DATA.name}}" placeholder="Enter name..."
			required />
		
		<!-- DATE : DATE -->
		<input type="date" name="date" id="setDate" class="form-control input-sm" />

	</div>
	
	<div name="submit" class="btn-group">

		<button type="submit" class="btn btn-primary btn-sm control-button">
			Pull records
		</button>
		
	</div>

</form>