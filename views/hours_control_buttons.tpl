


<div class="row">
	<div class="col-md-10">
		<div class="container-fluid" id="buttons">
		
			<div class="btn-group pull-left">
				<form action="/setName" method="post" class="form-inline" enctype="multipart/form-data">
					<div class="form-group">
						<input type="text" id="setName" name="setName" class="form-control" placeholder="Enter name..." />
					</div>
					<button type="submit" class="btn btn-info">Pull records</button>
				</form>
			</div>

		
			<div class="btn-group pull-right">
				<!-- DELETE RECORDS -->
				<form action="/delete" method="post" class="form-inline" enctype="multipart/form-data">						
					<div class="form-group">
						<input id="delete" name="delete" type="submit" value="Delete Records" class="btn btn-danger pull-right" onclick="confirmDelete()"/>
						<input id="deleteUser" name="deleteUser" type="hidden" value={{name}}/>
					</div>
				</form>
				<!-- EMAIL RECORDS -->
				<form action="/email" method="post" class="form-inline" enctype="multipart/form-data">
					<div class="form-group">						
						<input id="email" name="email" type="submit" value="Email Records" class="btn btn-success pull-right" onclick="confirmEmail()"/>
						<input id="emailUser" name="emailUser" type="hidden" value={{name}}/>
					</div>
				</form>
			</div> <!-- ./btn-group -->
		
		</div>
	</div>
</div>