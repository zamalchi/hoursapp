<%
import modu.labeler as labeler
import modu.recorder as recorder
%>

<!-- START OF PANEL-HEADING HTML -->

<div class="panel-heading"> 				
<div class="container-fluid">
<div class="row">
<div class="col-md-12" name="record-display-col">

	<div class="media">

		<div class="media-left media-middle" name="recordControls">
			<!-- TODO: needed in button? : data-index="{{ider.i}}" -->
			% include("button_collapse.tpl", record_id=ider.record())
			
			% include("button_delete.tpl", record_index=DISPLAY.index)
		</div>

		
		<div class="media-body" name="recordDisplay">

			<!-- anchor tag for adjusting page after editing a record -->
			<a name="{{DISPLAY.index}}"></a>

			<h4 class="panel-title pull-left" name="record-display-string">

			{{DISPLAY.record.name}} | {{DISPLAY.record.date}}

			<div name="start" class="record-content"><strong><u>{{DISPLAY.record.fstart}}</u></strong></div>

			| {{DISPLAY.record.date}}

			% if DISPLAY.record.isPending():
					
				% include("complete_end_form.tpl")

				| {{DISPLAY.record.duration}}

			% else:

				<div name="end" class="record-content"><strong><u>{{DISPLAY.record.fend}}</u></strong></div> |
				
				<div name="duration" class="record-content">

					% if float(DISPLAY.record.duration) <= 0:
						<span class="negative-duration">{{DISPLAY.record.duration}}</span>
					% else:
						{{DISPLAY.record.duration}}
					% end

				</div>

			% end

			|
			<div name="label" class="record-content">{{DISPLAY.record.label}}</div>
			|
			% include("toggle_display_billable.tpl", record=DISPLAY.record)
			| 
			% include("toggle_display_emergency.tpl", record=DISPLAY.record)				
			|
			<br>
			% include("complete_notes_form.tpl", record=DISPLAY.record)
			</h4>

		</div> <!-- /.media-body -->
	</div> <!-- /.media -->

</div>
</div>
</div>
</div>
