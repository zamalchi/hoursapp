

<script type="text/javascript">

// ####################################################################################################
// ####################################################################################################

function confirmDelete() {
	var choice = confirm("Are you sure you want to delete records?");
	if (choice) {
		document.getElementById("deleteConfirm").value = "true";
	}
}

function confirmEmail(self) {
	var sender = self.attributes['data-sender'].value;
	var receivers = self.attributes['data-receivers'].value;

	var choice = confirm("Sender: " + sender + "\n" + 
		"Receivers: " + receivers + "\n\n" +
		"Are you sure you want to email records?");
	if (choice) {
		document.getElementById("emailConfirm").value = "true";
	}
}

// ####################################################################################################
// ####################################################################################################


// gets element with provided id, sets value to "", and gives focus
function focusAndClearField(id) {
	var elem = document.getElementById(id);
	elem.value = "";
	elem.focus();
}


function adjustNextIndex(insertID, recordIndex) {
	document.getElementById(insertID).value = recordIndex;
}

// ####################################################################################################
// ####################################################################################################


function openViewer() {
	var str = document.getElementById("viewRecords").value;
	OpenWindow=window.open("", "newwin", "width=940, height=750, toolbar=no,scrollbars="+scroll+",menubar=no");
	OpenWindow.moveTo(0,0);
	OpenWindow.document.write(`
	<html>
	<head>
		<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css"/>
	 	<link rel="stylesheet" type="text/css" href="css/hours.css" />
		<title>Hours</title>
	</head>
	<body>
	<div class="container" id="viewerContents">
		<div class="row">
			<div class="col-md-6 col-md-offset-3">
				<div class="panel panel-default">
					<div class="panel-body">`);
	OpenWindow.document.write(str);
	OpenWindow.document.write(`
					</div>
				</div>
			</div>
		</div>
	</div>
	</body>
	</html>
	`);
	//var contents = document.getElementById("viewerContents");
	//OpenWindow.resizeTo(contents.offsetWidth, contents.offsetHeight);
	OpenWindow.document.close();
	self.name="main";
}

// ####################################################################################################
// ####################################################################################################


// private function
function setBillableEmergency(index, billable, emergency) {
	
	var b = "<strong>" + billable + "</strong>";
	var e = "<strong>" + emergency + "</strong>";

	var bill = document.getElementById("billable" + index);
	var b_span = bill.children[1];
	var b_hidden = bill.children[2];

	b_span.innerHTML = b;
	b_hidden.value = billable;

	var emer = document.getElementById("emergency" + index);
	var e_span = emer.children[1];
	var e_hidden = emer.children[2];

	e_span.innerHTML = e;
	e_hidden.value = emergency;
}


function toggleBE(self) {
	
	var c = self.children;

	var span = c[1];
	var hidden = c[2];

	if (hidden.value === "Y") {
		span.innerHTML = "<strong>N</strong>";
		hidden.value = "N";
	} else {
		hidden.value = "Y";
		span.innerHTML = "<strong>Y</strong>";
	}
}

// ####################################################################################################
// ####################################################################################################


function dropdownChangeSelect(self) {
	var index = self.attributes["data-index"].value;
	var selected = self.options[self.selectedIndex];

	var billable = selected.attributes["data-billable"].value
	var emergency = selected.attributes["data-emergency"].value

	setBillableEmergency(index, billable, emergency);

	// console.log(index, billable, emergency);
	// console.log(selected);

	var input = self.parentElement.querySelector("[name='dropdown']");
	input.value = self.options[self.selectedIndex].text;

	var value = self.parentElement.querySelector("[name='label']");
	value.value = self.options[self.selectedIndex].value;
}

function dropdownChangeType(self) {
	var index = self.attributes["data-index"].value;
	var names = self.attributes["data-name"].value;
	var billable = self.attributes["data-billable"].value;
	var emergency = self.attributes["data-emergency"].value;
	

	names = names.replace(/,|'|\[|\]/g, '').split(" ");
	billable = billable.replace(/,|'|\[|\]/g, '').split(" ");
	emergency = emergency.replace(/,|'|\[|\]/g, '').split(" ");

	var selected_index = names.indexOf(self.value.toUpperCase());

	if (selected_index >= 0) {
		setBillableEmergency(index, billable[selected_index], emergency[selected_index]);
	} else {
		setBillableEmergency(index, billable[0], emergency[0]);
	}


	var input = self.parentElement.querySelector("[name='dropdown']");
	var value = self.parentElement.querySelector("[name='label']");

	value.value = input.value;
}

// ####################################################################################################
// ####################################################################################################


function submitOnEnterPressed(event, formElem) {

	// if enter button was pressed, submit the form
	if (event.keyCode === 13) {
		formElem.submit();
	}
}

function setValueFromInnerText(self) {
	self.value = self.innerText;
}


</script>