<%
import modu.recorder as recorder
%>

<div class="row">
<div class="col-md-10">
<div class="container-fluid" id="header">

	<div class="row">
	<div class="col-md-12">
		<div class="panel panel-default">


			<div class="panel-heading">

					<div class="left">
						<h3 id="date-title">
							{{DATA.dateTitle}}
						</h3>
					</div>

					<div class="right">
						<h3 id="subtotal-counter">
							% if DATA.pendingRecordsExist:
								<span class="pending-text">* </span>
							% end
								Subtotal [Today]: <strong>{{DATA.subtotal}}</strong> [{{DATA.month}}]: <strong>{{DATA.total}}</strong>
						</h3>
					</div>

			</div>


			<div class="panel-body" id="controls">
				<div class="container-fluid">

				<div class="row" name="row1">
					<div class="col-lg-6 col-md-12 left">
						% include("header_pull.tpl")
					</div>
					<div class="col-lg-6 col-md-12 right">
						% include("header_right_buttons.tpl")
					</div>
				</div>

				<div class="row" name="row2">
					<div class="col-md-12">
						% include("header_send_records.tpl")
					</div>
				</div>

				</div>
			</div>


		</div>
	</div>
	</div>

</div>
</div>
</div>

