
<div class="row">
	<div class="col-md-10">
		<div class="container-fluid" id="buttons">
		
			<!-- SEARCH FOR RECORDS -->
			<div class="btn-group pull-left">
				<form action="/setCookies" method="post" class="form-inline" enctype="multipart/form-data">
					<div class="form-group">
						<input type="text" id="setName" name="setName" value="{{name}}" class="form-control input-sm third-width" placeholder="Enter name..." required />
						<input type="date" id="setDate" name="setDate" class="form-control input-sm" />
					</div>
					<button type="submit" class="btn btn-primary btn-sm">Pull records</button>
				</form>
			</div>

			<!-- VIEW RECORDS -->
			<div class="btn-group">
					<div class="form-group">
						<input id="view" name="view" type="submit" value="Formatted View" class="btn btn-info btn-sm pull-right" onclick="openViewer()" />
						<input id="viewRecords" name="viewRecords" type="hidden" value="{{!record_string}}" />
					</div>
			</div>

			<div class="btn-group pull-right">
				<!-- DELETE RECORDS -->
				<form action="/delete" method="post" class="form-inline" enctype="multipart/form-data">						
					<div class="form-group">
						<input id="delete" name="delete" type="submit" value="Delete" class="btn btn-danger btn-sm pull-right" onclick="confirmDelete()" />
						<input id="deleteConfirm" name="deleteConfirm" type="hidden" value="false" />
					</div>
				</form>
			</div>
			<div class="btn-group pull-right">
				<!-- EMAIL RECORDS -->
				<form action="/email" method="post" class="form-inline" enctype="multipart/form-data">
					<div class="form-group">						
						<input id="email" name="email" type="submit" value="Email" class="btn btn-success btn-sm pull-right" onclick="confirmEmail()" />
						<input id="emailUser" name="emailUser" type="hidden" value="{{name}}" />
					</div>
				</form>
			</div> <!-- ./btn-group -->
		
		</div>
	</div>
</div>

