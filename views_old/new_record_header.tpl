<%
import modu.labeler as labeler
%>

<div class="container-fluid">
<div class="row">
<div class="col-md-12" name="record-display-col">
<div class="media">

	<div class="media-left media-middle" name="recordControls">
		% include("button_collapse.tpl", record_id=ider.record())
	</div>


	<div class="media-body" name="recordDisplay">
		<h4 class="panel-title"><strong>Insert new record: #{{ider.i+1}}</strong></h4>
	</div>

</div>
</div>
</div>
</div>