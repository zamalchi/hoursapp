<div name="dropdown-wrapper">
	<div class="dropdown form-control">
		<!-- INITIAL VALUES USED FOR DEFAULT AND INDEX OFFSET -->
		<%
		ls_name = [""]
		ls_billable = ["Y"]
		ls_emergency = ["N"]

		for each in DATA.LABELS:
	  	l = each.split(" | ")
	  	ls_name.append(l[0])
	  	ls_billable.append(l[1])
	  	ls_emergency.append(l[2])
	  end
		%>
		<select class="dropdownSelect" data-index="{{ider.i}}" onchange="dropdownChangeSelect(this)" tabindex="4">
		   % for i, each in enumerate(ls_name):
		   	<option value="{{each}}" data-billable="{{ls_billable[i]}}" data-emergency="{{ls_emergency[i]}}">{{each}}</option>
		   % end
		</select>
		
		<input type="text" class="dropdownInput" name="{{namer.dropdown()}}" placeholder="Label" id="{{ider.dropdown()}}"
			onfocus="this.select()" onchange="dropdownChangeType(this)"
			data-name="{{ls_name}}" data-billable="{{ls_billable}}" data-emergency="{{ls_emergency}}" data-index="{{ider.i}}"
			required style="text-transform: uppercase;" tabindex="5" pattern="{{REGEX.LABELS}}" />
		
		<input name="{{namer.label()}}" id="{{ider.label()}}" type="hidden">
	</div>
</div>