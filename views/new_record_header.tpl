
<div class="panel-heading">
<div class="container-fluid">
<div class="row">
<div class="col-md-12" name="record-display-col">
<div class="media">

	<div class="media-left media-middle" name="recordControls">
		<!-- TODO: which one? what is the index of the new record? -->
		<!-- # % include("button_collapse.tpl", record_id=ider.record()) -->
		% include("button_collapse.tpl", recordId=HTML_LABELS.RECORD+str(index))
	</div>


	<div class="media-body" name="recordDisplay">
		<h4 class="panel-title"><strong>Insert new record: #{{len(DATA.records)+1}}</strong></h4>
	</div>

</div>
</div>
</div>
</div>
</div>