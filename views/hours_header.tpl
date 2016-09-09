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
						<div class="panel-heading" id="titles">
							
							<div class="container-fluid">
								<div class="row">

									<div class="col-md-12">

										<div name="left">
											<h3 id="dateTitle">
												{{date_title}}
											</h3>
										</div>

										<div name="right">
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

						</div>
						<!-- END OF PANEL-HEADING -->
						<!-- ################################################################# -->


						<!-- ################################################################# -->
						<!-- START OF PANEL-BODY : control buttons and inputs -->
						<div class="panel-body" id="controls">
							<div class="container-fluid">

								<div class="row">

									<!-- LEFT HALF START #####################################-->
									<div class="col-lg-6 col-md-12" name="left">

										<!-- SEARCH FOR RECORDS -->
											<form action="/setCookies" method="post" enctype="multipart/form-data">
												
												<div name="inputs">
													<input type="text" id="setName" name="setName" value="{{name}}" class="form-control input-sm"
														placeholder="Enter name..." required />
													
													<input type="date" id="setDate" name="setDate" class="form-control input-sm" />
												</div>
												
												<div name="submit" class="btn-group">
													<button type="submit" class="btn btn-primary btn-sm control-button">
														Pull records
													</button>
												</div>
											
											</form>

									</div>
									<!-- LEFT HALF END #######################################-->

									<!-- RIGHT HALF START ####################################-->
									<div class="col-lg-6 col-md-12" name="right">

										<div class="btn-group">
												
											<!-- VIEW FORMATTED RECORDS -->
											<div class="form-group inline-block button-wrapper">
												<input id="view" name="view" type="submit" value="Formatted" class="control-button btn btn-info btn-sm"
													onclick="openViewer()" />
												<input id="viewRecords" name="viewRecords" type="hidden" value="{{!record_string}}" />
											</div>
									
											<!-- VIEW UPDATES -->
											<div class="form-group inline-block button-wrapper">
												<a name="updates" href="/viewUpdates" target="__blank" class="control-button btn btn-default btn-sm">Updates</a>
											</div>


											<!-- DELETE RECORDS -->
											<form action="/delete" method="post" class="inline-block button-wrapper" enctype="multipart/form-data">						
												<div class="form-group full-width">
													
													<input id="delete" name="delete" type="submit" value="Delete" class="control-button btn btn-danger btn-sm"
														onclick="confirmDelete()" />
													
													<input id="deleteConfirm" name="deleteConfirm" type="hidden" value="false" />
												</div>
											</form>

											<!-- SEND RECORDS -->
											<form action="/send" method="post" class="inline-block button-wrapper" enctype="multipart/form-data">
												<div class="form-group full-width">						
													
													<input id="send" name="send" type="submit" value="Send" class="control-button btn btn-success btn-sm"
														onclick="confirmSend(this)" />
													
													<input id="sendConfirm" name="sendConfirm" type="hidden" value="false" />
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

