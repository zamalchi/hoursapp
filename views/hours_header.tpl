
<div class="row">
	<div class="col-md-10">
		<div class="container-fluid" id="header">

			<!-- ######################################################################################################### -->
			<!-- ######################################################################################################### -->

			<div class="row">
				<div class="col-md-12">

					<div class="panel panel-default">

						<!-- ################################################################# -->
						<!-- START OF PANEL-HEADING : date title and subtotal counters -->
						<div class="panel-heading">
							
							<div class="container-fluid">
								<div class="row">

									<div class="col-md-6 pull-left" id="dateTitle">
										<h3>{{date_title}}</h3>
									</div>

									<div class="col-md-6">
										<h3 id="subtotalCounter">
										% if pending_records:
											<span class="pending-text">* </span>
										% end
											Subtotal [Today]: <strong>{{daily_subtotal}}</strong> [{{month}}]: <strong>{{subtotal}}</strong>
										</h3>
									</div>

								</div>
							</div>

						</div>
						<!-- END OF PANEL-HEADING -->
						<!-- ################################################################# -->


						<!-- ################################################################# -->
						<!-- START OF PANEL-BODY : control buttons and inputs -->
						<div class="panel-body" id="controls">
							<div class="container-fluid">

								<div class="row">

									<!-- LEFT HALF START #####################################-->
									<div class="col-md-6">

										<!-- SEARCH FOR RECORDS -->
										<div class="btn-group">

											<form action="/setCookies" method="post" class="form-inline" enctype="multipart/form-data">
												<div class="form-group">
													
													<input type="text" id="setName" name="setName" value="{{name}}" class="form-control input-sm third-width" placeholder="Enter name..." required />
													
													<input type="date" id="setDate" name="setDate" class="form-control input-sm" />
												</div>
												
												<button type="submit" class="btn btn-primary btn-sm">Pull records</button>
											</form>

										</div>

									</div>
									<!-- LEFT HALF END #######################################-->

									<!-- RIGHT HALF START ####################################-->
									<div class="col-md-6">

										<div class="btn-group btn-group-sm">
												
											<!-- VIEW RECORDS -->
											<div class="form-group form-inline">
												<input id="view" name="view" type="submit" value="Formatted" class="control-button btn btn-info btn-sm"
													onclick="openViewer()" />
												<input id="viewRecords" name="viewRecords" type="hidden" value="{{!record_string}}" />
											</div>
									
											<!-- VIEW UPDATES -->
											% updates = ""
											% try:
												% f = open("UPDATES")
												% updates = f.read()
												% f.close()
											% except IOError:
												% updates = "Update file not found"
											% end

											<div class="form-group form-inline">
												<a href="/viewUpdates" target="__blank" class="control-button btn btn-default">Updates</a>
											</div>


											<!-- DELETE RECORDS -->
											<form action="/delete" method="post" class="form-inline" enctype="multipart/form-data">						
												<div class="form-group">
													<input id="delete" name="delete" type="submit" value="Delete" class="control-button btn btn-danger"
														onclick="confirmDelete()" />
													<input id="deleteConfirm" name="deleteConfirm" type="hidden" value="false" />
												</div>
											</form>

											<!-- EMAIL RECORDS -->
											<form action="/email" method="post" class="form-inline" enctype="multipart/form-data">
												<div class="form-group">						
													<input id="email" name="email" type="submit" value="Email" class="control-button btn btn-success"
														onclick="confirmEmail(this)" data-sender="{{sender}}" data-receivers="{{receivers}}" />
													<input id="emailConfirm" name="emailConfirm" type="hidden" value="false" />
												</div>
											</form>

										</div>

									</div>
									<!-- RIGHT HALF END ######################################-->


								</div>

							</div>
						</div>

						<!-- END OF PANEL-BODY -->
						<!-- ################################################################# -->
						

					</div>

				</div>
			</div>

			<!-- ######################################################################################################### -->
			<!-- ######################################################################################################### -->		
		
		</div>
	</div>
</div>

