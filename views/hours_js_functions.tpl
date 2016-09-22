

<script>

// goes to the anchor tag of the just-edited record or the top of page
$( document ).ready(function() {
	var i = String(document.body.attributes["data-index"].value);
	window.location.hash = i;

	var msg = String(document.body.attributes["data-server-response"].value);

	if (msg != "") { alert(msg); }

	// to prevent old values from being retained (ex submitting and then hitting back in the browser)
	document.getElementById("emailConfirm").value = "false";
	document.getElementById("sendConfirm").value = "false";

	var counter = $("#num-records").val();

	// if -1 (default value) --> open new record form
	if (i == "-1") { i = counter; }

	// // open the collapse form of the record corresponding to the anchor index	
	$("#record" + i).addClass("in");

	var name = $("#name" + i);
	var start = $("#start" + i);
	var end = $("#end" + i);

	if (name.val() == false) {
		name.focus();
	} else if (start.val() == false) {
		start.focus();
	} else if (end.val() == false) {
		end.focus();
	}

});

// ####################################################################################################
// ####################################################################################################

function confirmDelete() {
	var choice = confirm("Are you sure you want to delete records?");
	if (choice) {
		document.getElementById("deleteConfirm").value = "true";
	}
}

function confirmSend(self) {
	var choice = confirm("Are you sure you want to send records?")

	if (choice) {
		document.getElementById("sendConfirm").value = "true";
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
	<body name="viewer">
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

// for billable/emergency toggling
function toggleButtonPress(event, self) {
	event.preventDefault();
	// if enter or space button was pressed, toggle the billable/emergency element
	if (event.keyCode === 13 || event.keyCode === 32) {
		toggleBE(self);
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

// function modifyTimePattern(self) {
// 	minTime = self.attributes["data-min"].value;
// 	maxTime = self.attributes["data-max"].value;
// 	default_pattern = "(\s*|(0?[0-9]|1[0-9]|2[0-3]):?(00|15|30|45))";
// 	console.log(default_pattern);

// 	pattern="(\s*|(";

// 	if (minTime.substr(0,2) < 10) {
// 		pattern += "0?";
// 		pattern += "[" + minTime.substr(1,1) + "-";

// 		if (maxTime.substr(0,2) < 10) {
// 			pattern += maxTime.substr(1,1);
// 		} else {
// 			pattern += "9";
// 		}
// 		pattern += "]";
// 	}
// 	else if (minTime.substr(0,2) >= 10 && minTime.substr(0,2) < 20) {
// 		pattern += "1[" + minTime.substr(1,1) + "-";

// 		if (maxTime.substr(0,2) >= 10 && maxTime.substr(0,2) < 20) {
// 			pattern += maxTime.substr(1,1);
// 		} else {
// 			pattern += "9";
// 		}
// 		pattern += "]";
// 	}
// 	else if (minTime.substr(0,2) >= 20) {
// 		pattern += "|2[" + minTime.substr(1,1) + "-" + maxTime.substr(1,1);
// 	}
	
// 	pattern += "):?(";

// 	minuteArray = ["00", "15", "30", "45"];

// 	var minIndex = minuteArray.indexOf(minTime.substr(2,2));
// 	var maxIndex = minuteArray.indexOf(maxTime.substr(2,2));

// 	pattern += minuteArray.slice(minIndex, maxIndex+1).join("|") + "))";

// 	console.log(pattern);
// }

function checkTime(self) {
	var time = self.value.replace(":","");
	// pad with a leading 0, if missing
	if (time.length == 3) { time = '0' + time }
	var min = self.attributes["data-min"].value.replace(":","") || "0000";
	var max = self.attributes["data-max"].value.replace(":","") || "2345";

	if ((time != "") && (time <= min || time >= max)) {
		alert("Invalid time!\nTime (" + time + ") should be within the range: " + min + "-" + max + "\nTime must be at a quarter-hour interval");
	}

}

</script>